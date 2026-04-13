"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main

Loads the song catalog and runs recommendations for six user profiles:
three standard profiles and three adversarial/edge case profiles.
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Standard profiles
# ---------------------------------------------------------------------------

PROFILES = [
    (
        "Alex — Pop / Happy / High Energy",
        {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False},
    ),
    (
        "Sam — Lofi / Chill / Acoustic",
        {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    ),
    (
        "Jordan — EDM / Intense / High Energy",
        {"genre": "edm", "mood": "intense", "energy": 0.95, "likes_acoustic": False},
    ),
]

# ---------------------------------------------------------------------------
# Edge case / adversarial profiles
# Designed to expose weaknesses in the scoring logic
# ---------------------------------------------------------------------------

EDGE_PROFILES = [
    (
        "Riley — Conflicting Preferences (ambient genre + high energy)",
        # Ambient songs are all low energy, so genre and energy pull in opposite directions
        {"genre": "ambient", "mood": "chill", "energy": 0.9, "likes_acoustic": False},
    ),
    (
        "Morgan — Conflicting Preferences (acoustic folk + intense mood)",
        # Folk catalog has no intense songs, so mood match is impossible in preferred genre
        {"genre": "folk", "mood": "intense", "energy": 0.85, "likes_acoustic": True},
    ),
    (
        "Casey — Niche Genre with Low Catalog Coverage (country)",
        # Only one country song exists — tests what happens when the catalog runs dry
        {"genre": "country", "mood": "relaxed", "energy": 0.45, "likes_acoustic": True},
    ),
]


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a formatted block of top-k recommendations for one profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n{'=' * 60}")
    print(f"Profile: {profile_name}")
    print(f"  genre={user_prefs['genre']}  mood={user_prefs['mood']}  "
          f"energy={user_prefs['energy']}  acoustic={user_prefs['likes_acoustic']}")
    print(f"{'=' * 60}")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("\n--- Standard Profiles ---")
    for profile_name, user_prefs in PROFILES:
        print_recommendations(profile_name, user_prefs, songs)

    print("\n--- Edge Case / Adversarial Profiles ---")
    for profile_name, user_prefs in EDGE_PROFILES:
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()