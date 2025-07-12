const socket = io();  // Connects to server

const localVideo = document.getElementById("localVideo");
const remoteVideo = document.getElementById("remoteVideo");
let localStream;
let remoteStream;
let peerConnection;
const config = { iceServers: [{ urls: "stun:stun.l.google.com:19302" }] };

// Replace with actual values passed from HTML
const currentUser = window.currentUser;
const targetUser = window.targetUser;
const room = [currentUser, targetUser].sort().join('-');

// DOM elements
const startCallBtn = document.getElementById("startCall");
const shareScreenBtn = document.getElementById("shareScreen");
const muteBtn = document.getElementById("muteAudio");
const endCallBtn = document.getElementById("endCall");

// Join signaling room
socket.emit("join", { from: currentUser, to: targetUser });

// Start call
startCallBtn.onclick = async () => {
  localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
  localVideo.srcObject = localStream;

  setupPeerConnection();

  localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

  const offer = await peerConnection.createOffer();
  await peerConnection.setLocalDescription(offer);

  socket.emit("offer", { from: currentUser, to: targetUser, offer });
};

// Peer connection setup
function setupPeerConnection() {
  peerConnection = new RTCPeerConnection(config);

  peerConnection.onicecandidate = (e) => {
    if (e.candidate) {
      socket.emit("ice-candidate", { from: currentUser, to: targetUser, candidate: e.candidate });
    }
  };

  peerConnection.ontrack = (e) => {
    remoteVideo.srcObject = e.streams[0];
  };
}

// Handle incoming offer
socket.on("offer", async (offer) => {
  if (!peerConnection) {
    setupPeerConnection();
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    localVideo.srcObject = localStream;
    localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));
  }

  await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
  const answer = await peerConnection.createAnswer();
  await peerConnection.setLocalDescription(answer);
  socket.emit("answer", { from: currentUser, to: targetUser, answer });
});

// Handle incoming answer
socket.on("answer", async (answer) => {
  await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
});

// Handle ICE candidates
socket.on("ice-candidate", async (candidate) => {
  if (candidate && peerConnection) {
    try {
      await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
    } catch (err) {
      console.error("Error adding received ICE candidate", err);
    }
  }
});

// Share screen
shareScreenBtn.onclick = async () => {
  const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
  const screenTrack = screenStream.getVideoTracks()[0];
  const sender = peerConnection.getSenders().find(s => s.track.kind === 'video');
  if (sender) sender.replaceTrack(screenTrack);

  screenTrack.onended = async () => {
    // Revert to webcam after screen sharing ends
    const newStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    const newVideoTrack = newStream.getVideoTracks()[0];
    if (sender) sender.replaceTrack(newVideoTrack);
    localVideo.srcObject = newStream;
    localStream = newStream;
  };
};

// Mute/unmute toggle
muteBtn.onclick = () => {
  const audioTrack = localStream.getAudioTracks()[0];
  audioTrack.enabled = !audioTrack.enabled;
  muteBtn.textContent = audioTrack.enabled ? "Mute" : "Unmute";
};

// End call
endCallBtn.onclick = () => {
  if (peerConnection) {
    peerConnection.close();
    peerConnection = null;
  }
  localVideo.srcObject = null;
  remoteVideo.srcObject = null;
  socket.emit("end-call", { from: currentUser, to: targetUser });
};

// Handle remote call end
socket.on("end-call", () => {
  alert("Call ended by the other user.");
  if (peerConnection) {
    peerConnection.close();
    peerConnection = null;
  }
  localVideo.srcObject = null;
  remoteVideo.srcObject = null;
});