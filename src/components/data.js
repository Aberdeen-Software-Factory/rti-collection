const artifactList = [
  {
    id: "artifact-001",
    title: "Bronze Age Spearhead",
    description: "A Bronze Age spearhead with ornate engravings, likely used for ceremonial purposes.",
    images: [
      "/test/coin10.jpg",
      "/images/artifact-001-side.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
    ],
    relightableMedia: [
      {
        type: "RTI",
        url: "test-image"
      }
    ],
    creator: "Unknown",
    date: "c. 1200 BCE",
    copyright: "© Museum of Antiquities",
    tags: ["Bronze Age", "Weapon", "Ceremonial", "Engraving"]
  },
  {
    id: "artifact-002",
    title: "Roman Coin",
    description: "A Roman coin featuring Emperor Augustus. Minted in 27 BCE.",
    images: [
      "/images/artifact-002-front.jpg",
      "/images/artifact-002-back.jpg"
    ],
    relightableMedia: [
      {
        type: "RTI",
        url: "/relightable/artifact-002.rti"
      }
    ],
    creator: "Roman Empire",
    date: "27 BCE",
    copyright: "Public Domain",
    tags: ["Roman", "Coin", "Currency", "Augustus"]
  },
  {
    id: "artifact-003",
    title: "Medieval Manuscript Fragment",
    description: "A page from a medieval manuscript, written in Latin and illuminated with gold leaf.",
    images: [
      "/images/artifact-003.jpg",
      "/images/artifact-003-closeup.jpg"
    ],
    relightableMedia: [
      {
        type: "IIIF",
        url: "https://iiif.example.org/artifact-003/manifest.json"
      }
    ],
    creator: "Unknown Scribe",
    date: "c. 1350 CE",
    copyright: "© National Library",
    tags: ["Manuscript", "Medieval", "Illuminated", "Latin"]
  },
  {
    id: "artifact-004",
    title: "Ancient Greek Vase",
    description: "A red-figure amphora depicting a mythological battle scene.",
    images: [
      "/images/artifact-004-front.jpg",
      "/images/artifact-004-back.jpg"
    ],
    relightableMedia: [
      {
        type: "3D",
        url: "/3d/artifact-004.glb"
      }
    ],
    creator: "Attributed to the Berlin Painter",
    date: "c. 490 BCE",
    copyright: "© Archaeological Museum",
    tags: ["Greek", "Vase", "Ceramics", "Mythology"]
  },
  {
    id: "artifact-005",
    title: "Egyptian Scarab Amulet",
    description: "A small scarab amulet used for protection in the afterlife.",
    images: [
      "/images/artifact-005.jpg",
      "/images/artifact-005-reverse.jpg"
    ],
    relightableMedia: [
      {
        type: "RTI",
        url: "/relightable/artifact-005.rti"
      },
      {
        type: "Photogrammetry",
        url: "/3d/artifact-005.glb"
      }
    ],
    creator: "Ancient Egyptian Artisan",
    date: "c. 1500 BCE",
    copyright: "© Cairo Museum",
    tags: ["Egyptian", "Amulet", "Scarab", "Funerary"]
  }
];

export default artifactList;
