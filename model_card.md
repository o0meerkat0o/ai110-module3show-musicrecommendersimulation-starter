# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Goal / Task

VibeFinder suggests songs from a 20-song catalog that match a listener's preferred genre, mood, energy level, and acoustic preference. Given a user profile with those four values, it returns the top 5 best-matching songs along with a plain-language explanation for each one. It is designed for classroom exploration of content-based filtering, not for real-world music platforms.

---

## 3. Data Used

The catalog contains 20 songs across 12 genres (pop, rock, lofi, jazz, edm, hip-hop, folk, country, r&b, ambient, synthwave, indie pop) and 6 moods (happy, chill, intense, moody, relaxed, focused). Each song has 8 attributes: title, artist, genre, mood, energy (0.0–1.0), tempo in BPM, valence (0.0–1.0), danceability (0.0–1.0), and acousticness (0.0–1.0). The dataset is small and reflects a broadly Western pop music frame. Several genres like country and folk have only one or two songs, which limits recommendation quality for users who prefer those genres.

---

## 4. Algorithm Summary

For each song in the catalog, the system computes a score by checking four things. First, if the song's genre matches the user's preferred genre, it earns 3 points — the highest weight because genre is the strongest predictor of taste. Second, if the mood matches, it earns 2 more points. Third, the system measures how close the song's energy level is to the user's target: a perfect match earns 1.5 points and anything slightly off earns proportionally less. Fourth, if the song's acoustic character (organic vs. electronic) fits the user's preference, it earns 1 more point. All four contributions are added together and songs are sorted from highest to lowest score. The top results are returned with a written explanation of exactly which factors contributed points.

---

## 5. Observed Behavior / Biases

The genre weight (3.0) is strong enough to dominate the score in most cases. Two songs that match the preferred genre will usually outscore a perfect mood-and-energy match in a different genre. This creates a filter bubble: users rarely see songs outside their stated genre even when those would be a better emotional fit. A second bias is catalog sparsity — genres with only one song (country, folk) produce one strong recommendation followed by weak fallbacks in unrelated genres. A third issue is that the system cannot detect conflicting preferences: a user who asks for high-energy ambient music gets the two lowest-energy songs in the catalog because they happen to be the only ambient ones, with no warning that the request was contradictory.

---

## 6. Evaluation Process

Six user profiles were tested: three standard (pop/happy, lofi/chill, edm/intense) and three adversarial (ambient+high energy, folk+intense, country/relaxed). Standard profiles produced sensible results with scores in the 7.4–7.5 range for the top match. The adversarial profiles revealed the filter bubble and conflict-blindness issues described above. The most surprising result was the Riley profile: requesting high-energy ambient music returned the two quietest songs in the catalog, the exact opposite of the energy target, because genre weight alone was enough to push them to the top. A weight-shift experiment (lowering genre weight, raising energy weight) confirmed this — Riley's results shifted toward higher-energy songs when genre stopped dominating.

---

## 7. Intended Use and Non-Intended Use

**Intended use:** Classroom demonstration of how content-based filtering works. Suitable for exploring how scoring weights affect recommendations and where simple algorithms break down.

**Not intended for:** Real music platforms, production use, or any context where recommendations affect actual users. The catalog is too small, the preference model is too simple, and there is no feedback loop or personalization over time.

---

## 8. Ideas for Improvement

1. **Conflict detection:** Before scoring, check whether the user's genre and energy preferences are compatible given the catalog. If no songs in the preferred genre match the energy target within a reasonable range, warn the user rather than silently returning bad results.
2. **User-adjustable weights:** Let users set their own importance values per session (e.g., "mood matters more than genre today") so the system adapts to context rather than using fixed weights.
3. **Larger, more balanced catalog:** Add at least 3–5 songs per genre so niche-genre users get meaningful ranked results beyond rank 1.

---

## 9. Personal Reflection

Building this made me realize how much a single design choice — like setting the genre weight to 3.0 — can quietly control everything the system does, even when other features like energy or mood seem equally important. The most surprising result was the Riley edge case, where a user asking for high-energy ambient music got the exact opposite because the genre weight forced ambient songs to the top regardless of their energy. I also didn't expect how quickly a 20-song catalog would run out of meaningful options for niche genres like country or folk — it made the limitations of small datasets feel very concrete. Thinking about this in the context of real apps like Spotify, I now notice how much those platforms must rely on massive catalogs and user feedback loops to avoid the filter bubbles our simple scoring logic creates so easily.