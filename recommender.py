import numpy as np
from songs_db import SONGS

ALL_TAGS = [
    "main_character", "rotting", "villain", "healing",
    "down_bad", "unbothered", "chaotic", "in_denial",
    "obsessive", "curated", "chaotic_shuffle", "unhinged_creative",
    "gremlin", "emotional", "dreamer", "healthy",
    "gen_z_text", "hype_energy", "oversharer", "aloof"
]

TAG_INDEX = {tag: i for i, tag in enumerate(ALL_TAGS)}


def vectorize_tags(tags: list[str]) -> np.ndarray:
    vec = np.zeros(len(ALL_TAGS))
    for tag in tags:
        if tag in TAG_INDEX:
            vec[TAG_INDEX[tag]] = 1.0
    return vec


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def recommend(user_tags: list[str], genre_filter: str = None, top_k: int = 5) -> list[dict]:
    user_vec = vectorize_tags(user_tags)

    scored = []
    for song in SONGS:
        if genre_filter and song["genre"].lower() != genre_filter.lower():
            continue
        song_vec = vectorize_tags(song["tags"])
        score = cosine_similarity(user_vec, song_vec)
        scored.append({**song, "score": round(score, 4)})

    scored.sort(key=lambda x: x["score"], reverse=True)

    # if genre filter returns nothing, fall back to all songs
    if not scored:
        return recommend(user_tags, genre_filter=None, top_k=top_k)

    return scored[:top_k]


def get_top_match(user_tags: list[str], genre_filter: str = None) -> dict:
    results = recommend(user_tags, genre_filter)
    return results[0] if results else None


if __name__ == "__main__":
    # quick test
    test_tags = ["villain", "unbothered", "aloof", "healthy"]
    print("Test tags:", test_tags)
    print("\nTop 3 matches:")
    for r in recommend(test_tags, top_k=3):
        print(f"  {r['score']:.3f}  {r['song']} — {r['artist']}  [{r['genre']}]")
