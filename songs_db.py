
SONGS = [
    # ── Pop ──────────────────────────────────────────────────────────────
    {"song": "Espresso", "artist": "Sabrina Carpenter", "genre": "Pop",
     "tags": ["main_character", "unbothered", "curated", "aloof", "healthy"],
     "energy": 0.85, "valence": 0.9, "vibe": "that girl energy"},

    {"song": "Nonsense", "artist": "Sabrina Carpenter", "genre": "Pop",
     "tags": ["main_character", "down_bad", "chaotic", "hype_energy", "healthy"],
     "energy": 0.8, "valence": 0.88, "vibe": "flirty chaos"},

    {"song": "Please Please Please", "artist": "Sabrina Carpenter", "genre": "Pop",
     "tags": ["down_bad", "oversharer", "obsessive", "chaotic", "emotional"],
     "energy": 0.78, "valence": 0.72, "vibe": "begging era"},

    {"song": "Flowers", "artist": "Miley Cyrus", "genre": "Pop",
     "tags": ["healing", "unbothered", "villain", "curated", "gen_z_text"],
     "energy": 0.75, "valence": 0.82, "vibe": "self-love era"},

    {"song": "Cruel Summer", "artist": "Taylor Swift", "genre": "Pop",
     "tags": ["down_bad", "main_character", "obsessive", "dreamer", "oversharer"],
     "energy": 0.9, "valence": 0.7, "vibe": "pining chaos"},

    {"song": "Anti-Hero", "artist": "Taylor Swift", "genre": "Pop",
     "tags": ["rotting", "healing", "emotional", "oversharer", "gen_z_text"],
     "energy": 0.6, "valence": 0.45, "vibe": "self-aware spiral"},

    {"song": "Midnight Rain", "artist": "Taylor Swift", "genre": "Pop",
     "tags": ["dreamer", "emotional", "in_denial", "rotting", "curated"],
     "energy": 0.5, "valence": 0.4, "vibe": "wistful daydream"},

    {"song": "Shake It Off", "artist": "Taylor Swift", "genre": "Pop",
     "tags": ["unbothered", "healthy", "hype_energy", "main_character", "chaotic_shuffle"],
     "energy": 0.92, "valence": 0.95, "vibe": "unbothered queen"},

    {"song": "Popular", "artist": "The Weeknd ft. Madonna & Playboi Carti", "genre": "Pop",
     "tags": ["villain", "main_character", "aloof", "hype_energy", "curated"],
     "energy": 0.86, "valence": 0.65, "vibe": "effortlessly cool"},

    {"song": "Die With A Smile", "artist": "Lady Gaga & Bruno Mars", "genre": "Pop",
     "tags": ["emotional", "dreamer", "down_bad", "oversharer", "healing"],
     "energy": 0.62, "valence": 0.68, "vibe": "beautifully dramatic"},

    {"song": "APT.", "artist": "ROSÉ & Bruno Mars", "genre": "Pop",
     "tags": ["chaotic", "down_bad", "hype_energy", "main_character", "obsessive"],
     "energy": 0.88, "valence": 0.85, "vibe": "addicted and thriving"},

    # ── Hip-Hop ───────────────────────────────────────────────────────────
    {"song": "Not Like Us", "artist": "Kendrick Lamar", "genre": "Hip-Hop",
     "tags": ["villain", "unbothered", "hype_energy", "curated", "aloof"],
     "energy": 0.95, "valence": 0.6, "vibe": "certified villain"},

    {"song": "Luther", "artist": "Kendrick Lamar ft. SZA", "genre": "Hip-Hop",
     "tags": ["obsessive", "down_bad", "dreamer", "emotional", "oversharer"],
     "energy": 0.55, "valence": 0.65, "vibe": "soft obsessive"},

    {"song": "Rich Flex", "artist": "Drake & 21 Savage", "genre": "Hip-Hop",
     "tags": ["main_character", "villain", "hype_energy", "chaotic_shuffle", "aloof"],
     "energy": 0.88, "valence": 0.72, "vibe": "flexing on everyone"},

    {"song": "fukumean", "artist": "Gunna", "genre": "Hip-Hop",
     "tags": ["villain", "unbothered", "aloof", "healthy", "chaotic_shuffle"],
     "energy": 0.82, "valence": 0.68, "vibe": "unbothered villain"},

    {"song": "Carnival", "artist": "¥$, Kanye West & Ty Dolla $ign", "genre": "Hip-Hop",
     "tags": ["villain", "unhinged_creative", "chaotic", "hype_energy", "obsessive"],
     "energy": 0.9, "valence": 0.55, "vibe": "chaotic genius energy"},

    {"song": "Thinkin Bout Me", "artist": "Morgan Wallen", "genre": "Hip-Hop",
     "tags": ["in_denial", "rotting", "down_bad", "aloof", "gen_z_text"],
     "energy": 0.65, "valence": 0.42, "vibe": "quietly spiraling"},

    {"song": "Money Trees", "artist": "Kendrick Lamar", "genre": "Hip-Hop",
     "tags": ["dreamer", "curated", "emotional", "healing", "healthy"],
     "energy": 0.7, "valence": 0.58, "vibe": "ambitious daydream"},

    # ── R&B ───────────────────────────────────────────────────────────────
    {"song": "Good Days", "artist": "SZA", "genre": "R&B",
     "tags": ["healing", "dreamer", "emotional", "gen_z_text", "rotting"],
     "energy": 0.45, "valence": 0.5, "vibe": "hopeful melancholy"},

    {"song": "Kill Bill", "artist": "SZA", "genre": "R&B",
     "tags": ["obsessive", "down_bad", "villain", "oversharer", "emotional"],
     "energy": 0.65, "valence": 0.4, "vibe": "unhinged in love"},

    {"song": "Snooze", "artist": "SZA", "genre": "R&B",
     "tags": ["down_bad", "dreamer", "obsessive", "emotional", "oversharer"],
     "energy": 0.5, "valence": 0.55, "vibe": "lovesick and aware"},

    {"song": "Saturn", "artist": "SZA", "genre": "R&B",
     "tags": ["healing", "dreamer", "emotional", "curated", "gen_z_text"],
     "energy": 0.48, "valence": 0.62, "vibe": "cosmic healing"},

    {"song": "Creepin'", "artist": "Metro Boomin ft. The Weeknd", "genre": "R&B",
     "tags": ["chaotic", "in_denial", "gremlin", "aloof", "villain"],
     "energy": 0.7, "valence": 0.38, "vibe": "late night chaos"},

    {"song": "Here We Go (Uh Oh)", "artist": "Jazmine Sullivan", "genre": "R&B",
     "tags": ["oversharer", "down_bad", "in_denial", "emotional", "rotting"],
     "energy": 0.58, "valence": 0.35, "vibe": "self-aware disaster"},

    {"song": "Essence", "artist": "Wizkid ft. Tems", "genre": "R&B",
     "tags": ["dreamer", "down_bad", "healing", "curated", "emotional"],
     "energy": 0.72, "valence": 0.8, "vibe": "smooth obsession"},

    # ── Indie ─────────────────────────────────────────────────────────────
    {"song": "as it was", "artist": "Harry Styles", "genre": "Indie",
     "tags": ["healing", "emotional", "dreamer", "gen_z_text", "rotting"],
     "energy": 0.62, "valence": 0.52, "vibe": "healing but unwell"},

    {"song": "Everywhere, Everything", "artist": "Noah Kahan", "genre": "Indie",
     "tags": ["down_bad", "oversharer", "dreamer", "emotional", "obsessive"],
     "energy": 0.55, "valence": 0.6, "vibe": "soft romantic chaos"},

    {"song": "Stick Season", "artist": "Noah Kahan", "genre": "Indie",
     "tags": ["rotting", "emotional", "dreamer", "in_denial", "gen_z_text"],
     "energy": 0.5, "valence": 0.35, "vibe": "seasonal depression pop"},

    {"song": "Supernatural", "artist": "Gracie Abrams", "genre": "Indie",
     "tags": ["obsessive", "down_bad", "oversharer", "dreamer", "emotional"],
     "energy": 0.48, "valence": 0.42, "vibe": "quietly unraveling"},

    {"song": "I Love You, I'm Sorry", "artist": "Gracie Abrams", "genre": "Indie",
     "tags": ["oversharer", "healing", "emotional", "in_denial", "down_bad"],
     "energy": 0.4, "valence": 0.3, "vibe": "soft devastation"},

    {"song": "Ribs", "artist": "Lorde", "genre": "Indie",
     "tags": ["dreamer", "gremlin", "unhinged_creative", "emotional", "rotting"],
     "energy": 0.55, "valence": 0.28, "vibe": "existential teenager"},

    {"song": "Royals", "artist": "Lorde", "genre": "Indie",
     "tags": ["unbothered", "aloof", "gen_z_text", "villain", "curated"],
     "energy": 0.6, "valence": 0.5, "vibe": "cool outsider energy"},

    {"song": "Liability", "artist": "Lorde", "genre": "Indie",
     "tags": ["rotting", "in_denial", "emotional", "oversharer", "dreamer"],
     "energy": 0.3, "valence": 0.2, "vibe": "too much and proud"},

    {"song": "Featherweight", "artist": "boygenius", "genre": "Indie",
     "tags": ["healing", "emotional", "dreamer", "gen_z_text", "curated"],
     "energy": 0.42, "valence": 0.45, "vibe": "gentle devastation"},

    # ── Electronic ────────────────────────────────────────────────────────
    {"song": "Escapism.", "artist": "RAYE ft. 070 Shake", "genre": "Electronic",
     "tags": ["gremlin", "chaotic", "villain", "rotting", "hype_energy"],
     "energy": 0.78, "valence": 0.35, "vibe": "spiraling in the club"},

    {"song": "Redlight", "artist": "Sub Focus & Dimension", "genre": "Electronic",
     "tags": ["chaotic_shuffle", "hype_energy", "healthy", "main_character", "curated"],
     "energy": 0.92, "valence": 0.75, "vibe": "main character montage"},

    {"song": "Rumors", "artist": "Sabrina Carpenter", "genre": "Electronic",
     "tags": ["villain", "unbothered", "aloof", "curated", "main_character"],
     "energy": 0.8, "valence": 0.7, "vibe": "unbothered icon"},

    {"song": "Levitating", "artist": "Dua Lipa", "genre": "Electronic",
     "tags": ["main_character", "hype_energy", "healthy", "chaotic_shuffle", "dreamer"],
     "energy": 0.88, "valence": 0.88, "vibe": "floating in serotonin"},

    {"song": "Illusion", "artist": "Dua Lipa", "genre": "Electronic",
     "tags": ["villain", "aloof", "unbothered", "curated", "main_character"],
     "energy": 0.83, "valence": 0.75, "vibe": "cold and magnetic"},

    {"song": "Chemical", "artist": "Post Malone", "genre": "Electronic",
     "tags": ["down_bad", "obsessive", "gremlin", "chaotic", "in_denial"],
     "energy": 0.75, "valence": 0.4, "vibe": "addicted and spiraling"},

    # ── Sad Girl ─────────────────────────────────────────────────────────
    {"song": "Bags", "artist": "Clairo", "genre": "Sad Girl",
     "tags": ["down_bad", "gen_z_text", "dreamer", "obsessive", "emotional"],
     "energy": 0.3, "valence": 0.38, "vibe": "soft down bad"},

    {"song": "Pretty Girl", "artist": "Clairo", "genre": "Sad Girl",
     "tags": ["healing", "rotting", "gen_z_text", "dreamer", "in_denial"],
     "energy": 0.28, "valence": 0.42, "vibe": "bedroom melancholy"},

    {"song": "Motion Sickness", "artist": "Phoebe Bridgers", "genre": "Sad Girl",
     "tags": ["emotional", "oversharer", "healing", "in_denial", "dreamer"],
     "energy": 0.55, "valence": 0.3, "vibe": "artfully devastated"},

    {"song": "Moon Song", "artist": "Phoebe Bridgers", "genre": "Sad Girl",
     "tags": ["obsessive", "down_bad", "dreamer", "emotional", "rotting"],
     "energy": 0.25, "valence": 0.22, "vibe": "lovesick beyond repair"},

    {"song": "funeral", "artist": "Phoebe Bridgers", "genre": "Sad Girl",
     "tags": ["rotting", "dreamer", "gremlin", "emotional", "unhinged_creative"],
     "energy": 0.3, "valence": 0.18, "vibe": "beautifully broken"},

    {"song": "amoeba", "artist": "Clairo", "genre": "Sad Girl",
     "tags": ["gen_z_text", "aloof", "in_denial", "rotting", "dreamer"],
     "energy": 0.22, "valence": 0.3, "vibe": "drifting softly"},

    {"song": "Sofia", "artist": "Clairo", "genre": "Sad Girl",
     "tags": ["down_bad", "obsessive", "emotional", "dreamer", "oversharer"],
     "energy": 0.32, "valence": 0.35, "vibe": "quietly obsessed"},

    # ── K-Pop ─────────────────────────────────────────────────────────────
    {"song": "Magnetic", "artist": "ILLIT", "genre": "K-Pop",
     "tags": ["main_character", "hype_energy", "curated", "healthy", "unbothered"],
     "energy": 0.88, "valence": 0.85, "vibe": "effortlessly iconic"},

    {"song": "Seven", "artist": "Jung Kook ft. Latto", "genre": "K-Pop",
     "tags": ["down_bad", "chaotic", "gremlin", "hype_energy", "obsessive"],
     "energy": 0.85, "valence": 0.78, "vibe": "chaotic in love"},

    {"song": "Supernova", "artist": "aespa", "genre": "K-Pop",
     "tags": ["main_character", "villain", "hype_energy", "curated", "unbothered"],
     "energy": 0.9, "valence": 0.8, "vibe": "otherworldly icon"},

    {"song": "How Sweet", "artist": "NewJeans", "genre": "K-Pop",
     "tags": ["healing", "main_character", "healthy", "curated", "dreamer"],
     "energy": 0.72, "valence": 0.85, "vibe": "soft & sweet energy"},

    {"song": "Whiplash", "artist": "aespa", "genre": "K-Pop",
     "tags": ["villain", "chaotic", "hype_energy", "main_character", "aloof"],
     "energy": 0.92, "valence": 0.7, "vibe": "lethal confidence"},

    {"song": "OMG", "artist": "NewJeans", "genre": "K-Pop",
     "tags": ["chaotic", "down_bad", "obsessive", "hype_energy", "gen_z_text"],
     "energy": 0.82, "valence": 0.8, "vibe": "obsessed and cute about it"},

    # ── Latin ─────────────────────────────────────────────────────────────
    {"song": "Shakira: Bzrp Music Sessions #53", "artist": "Bizarrap & Shakira", "genre": "Latin",
     "tags": ["villain", "unbothered", "healing", "main_character", "aloof"],
     "energy": 0.82, "valence": 0.72, "vibe": "revenge served cold"},

    {"song": "La Bebe", "artist": "Yng Lvcas & Peso Pluma", "genre": "Latin",
     "tags": ["main_character", "hype_energy", "chaotic_shuffle", "healthy", "curated"],
     "energy": 0.9, "valence": 0.88, "vibe": "zero apologies"},

    {"song": "El Azul", "artist": "Bad Bunny & Jhayco", "genre": "Latin",
     "tags": ["dreamer", "down_bad", "emotional", "curated", "healing"],
     "energy": 0.65, "valence": 0.6, "vibe": "romantic nostalgia"},

    {"song": "MONACO", "artist": "Bad Bunny", "genre": "Latin",
     "tags": ["villain", "unbothered", "aloof", "main_character", "healthy"],
     "energy": 0.88, "valence": 0.75, "vibe": "elevated and untouchable"},

    # ── Afrobeats ────────────────────────────────────────────────────────
    {"song": "Calm Down", "artist": "Rema & Selena Gomez", "genre": "Afrobeats",
     "tags": ["down_bad", "main_character", "chaotic", "hype_energy", "obsessive"],
     "energy": 0.84, "valence": 0.82, "vibe": "obsessed and thriving"},

    {"song": "Water", "artist": "Tyla", "genre": "Afrobeats",
     "tags": ["main_character", "unbothered", "curated", "healthy", "aloof"],
     "energy": 0.8, "valence": 0.85, "vibe": "effortless magnetism"},

    {"song": "Angel", "artist": "Tyla ft. BEAM", "genre": "Afrobeats",
     "tags": ["dreamer", "healing", "emotional", "curated", "down_bad"],
     "energy": 0.7, "valence": 0.75, "vibe": "tender obsession"},

    # ── Rock ─────────────────────────────────────────────────────────────
    {"song": "Vampire", "artist": "Olivia Rodrigo", "genre": "Rock",
     "tags": ["villain", "healing", "oversharer", "emotional", "in_denial"],
     "energy": 0.78, "valence": 0.3, "vibe": "poetic chaos"},

    {"song": "good 4 u", "artist": "Olivia Rodrigo", "genre": "Rock",
     "tags": ["villain", "chaotic", "hype_energy", "healing", "unbothered"],
     "energy": 0.9, "valence": 0.45, "vibe": "passive aggressive icon"},

    {"song": "brutal", "artist": "Olivia Rodrigo", "genre": "Rock",
     "tags": ["rotting", "gen_z_text", "gremlin", "chaotic", "oversharer"],
     "energy": 0.88, "valence": 0.38, "vibe": "chaotic teen spirit"},

    {"song": "Making the Bed", "artist": "Olivia Rodrigo", "genre": "Rock",
     "tags": ["healing", "in_denial", "oversharer", "emotional", "dreamer"],
     "energy": 0.65, "valence": 0.42, "vibe": "reluctant growth era"},

    {"song": "Espresso (Rock Edit)", "artist": "Paramore", "genre": "Rock",
     "tags": ["main_character", "hype_energy", "healthy", "curated", "unbothered"],
     "energy": 0.93, "valence": 0.7, "vibe": "power walk energy"},

    {"song": "Misery Business", "artist": "Paramore", "genre": "Rock",
     "tags": ["villain", "chaotic", "hype_energy", "main_character", "healing"],
     "energy": 0.95, "valence": 0.5, "vibe": "classic chaos queen"},

    {"song": "That's So True", "artist": "Gracie Abrams", "genre": "Rock",
     "tags": ["healing", "emotional", "oversharer", "gen_z_text", "in_denial"],
     "energy": 0.6, "valence": 0.48, "vibe": "soft catharsis"},
]
