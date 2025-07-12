import difflib
from backend.database.database_utils import load_clients_from_db

def skills_match_fuzzy(skill_list_a, skill_list_b, threshold=0.3):
    """
    Returns True if any skill in A loosely matches any skill in B based on similarity ratio.
    """
    for skill_a in skill_list_a:
        for skill_b in skill_list_b:
            ratio = difflib.SequenceMatcher(None, skill_a.lower(), skill_b.lower()).ratio()
            if ratio >= threshold:
                return True
    return False

def get_skill_matches(current_user):
    all_clients = load_clients_from_db()
    matches = []

    for other in all_clients:
        if other.username == current_user.username:
            continue

        # Convert to lists and strip whitespace
        current_teach = [s.strip() for s in current_user.teach_skills.split(',')]
        current_learn = [s.strip() for s in current_user.learn_skills.split(',')]
        other_teach = [s.strip() for s in other.teach_skills.split(',')]
        other_learn = [s.strip() for s in other.learn_skills.split(',')]

        teach_match = skills_match_fuzzy(current_learn, other_teach)
        learn_match = skills_match_fuzzy(current_teach, other_learn)

        if teach_match and learn_match:
            matches.append(other)

    return matches