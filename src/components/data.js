const artifactList = [
  {
    id: "artifact-001",
    title: "Abibaal",
    description: "A rare gold coin from antiquity, likely used in high-value trade or ceremonial offerings.",
    images: [
      "/test/coin10.jpg",
      "/img/1.jpg",
      "/img/2.jpg",
      "/img/3.jpg",
      "/img/4.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
      "/images/artifact-001-detail.jpg",
    ],
    relightableMedia: [
      {
        type: "RTI",
        url: "http://localhost:8000/files/artifacts/6fdf38bc-606e-4632-8425-7eea52e25bf9/rti/fa33d74e-8a96-4965-abd8-f3326ad0965d/info.json",
        thumbnail: "rti/abibaal/Abibaal_1000/Abibaal_1000.jpg"
      },
      {
        type: "RTI",
        url: "rti/abibaal/Abibaal_1000/info.json",
        thumbnail: "rti/abibaal/Abibaal_1000/Abibaal_1000.jpg"
      },
      {
        type: "RTI",
        url: "rti/abibaal/Abibaal_side_01_fullsize/info.json",
        thumbnail: "rti/abibaal/Abibaal_side_01_fullsize/thumbnail.jpg"
      },
      {
        type: "RTI",
        url: "test/ptm/info.json"
      },
    ],
    creator: "Unknown",
    date: "c. 600 BCE",
    copyright: "© Museum of Antiquities",
    tags: ["Gold", "Coin", "Ancient", "Currency"]
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
        url: "test-image"
      },
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
