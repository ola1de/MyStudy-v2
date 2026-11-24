// Hand-built SVG scene for the homepage masthead: an open book, a
// graduation cap, stacked books and a pencil — drawn from the v1 palette
// (primary #5b57e8, dark navy #181a3d, amber #d97706). No stock photo,
// no gradient blob, no AI-looking hero art.
export default function HeroArt() {
  return (
    <svg
      viewBox="0 0 460 340"
      width="100%"
      height="auto"
      role="img"
      aria-label="An open book with a graduation cap, stacked books and a pencil"
      className="hero-art"
    >
      {/* sun */}
      <circle cx="392" cy="52" r="26" fill="#fbbf24" />
      <g stroke="#f59e0b" strokeWidth="3" strokeLinecap="round">
        <path d="M392 14v8M392 82v8M354 52h8M422 52h8M365 25l6 6M413 73l6 6M419 25l-6 6M371 73l-6 6" />
      </g>
      {/* dotted path */}
      <path
        d="M40 300 C 120 270, 180 320, 260 292 S 400 250, 424 268"
        fill="none"
        stroke="#5b57e8"
        strokeWidth="2"
        strokeDasharray="2 8"
        strokeLinecap="round"
      />
      {/* stacked books, left */}
      <g>
        <rect x="28" y="238" width="120" height="20" rx="3" fill="#181a3d" />
        <rect x="28" y="238" width="10" height="20" fill="#5b57e8" />
        <rect x="36" y="218" width="106" height="20" rx="3" fill="#5b57e8" />
        <rect x="36" y="218" width="10" height="20" fill="#181a3d" />
        <rect x="44" y="198" width="92" height="20" rx="3" fill="#d97706" />
        <rect x="44" y="198" width="10" height="20" fill="#fff" opacity="0.55" />
      </g>
      {/* open book */}
      <g>
        <path d="M150 120 C 190 96, 230 96, 262 118 L 262 252 C 230 230, 190 230, 150 252 Z" fill="#ffffff" stroke="#181a3d" strokeWidth="3" strokeLinejoin="round" />
        <path d="M374 120 C 334 96, 294 96, 262 118 L 262 252 C 294 230, 334 230, 374 252 Z" fill="#f4f5f8" stroke="#181a3d" strokeWidth="3" strokeLinejoin="round" />
        <path d="M262 118 V 252" stroke="#181a3d" strokeWidth="3" />
        <g stroke="#5b57e8" strokeWidth="3" strokeLinecap="round">
          <path d="M168 140 C 196 128, 220 128, 244 140" />
          <path d="M168 166 C 196 154, 220 154, 244 166" />
          <path d="M168 192 C 196 180, 220 180, 244 192" />
          <path d="M280 140 C 304 128, 328 128, 356 140" />
          <path d="M280 166 C 304 154, 328 154, 356 166" />
          <path d="M280 192 C 304 180, 328 180, 356 192" />
        </g>
        {/* tick + cross marks on the page, like a marked script */}
        <path d="M186 214 l6 6 12-14" fill="none" stroke="#15803d" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M322 210 l14 14 M336 210 l-14 14" stroke="#dc2626" strokeWidth="3" strokeLinecap="round" />
      </g>
      {/* graduation cap */}
      <g>
        <path d="M262 34 L 372 78 L 262 122 L 152 78 Z" fill="#181a3d" />
        <path d="M262 34 L 372 78 L 262 122 L 152 78 Z" fill="none" stroke="#181a3d" strokeWidth="3" strokeLinejoin="round" />
        <path d="M206 96 V 138 C 206 156, 318 156, 318 138 V 96 L 262 122 Z" fill="#5b57e8" />
        <path d="M372 78 V 132" stroke="#d97706" strokeWidth="3" strokeLinecap="round" />
        <circle cx="372" cy="140" r="7" fill="#d97706" />
        <path d="M262 34 L 372 78 L 262 122 L 152 78 Z" fill="#181a3d" opacity="0.08" />
      </g>
      {/* pencil */}
      <g transform="rotate(38 392 250)">
        <rect x="384" y="196" width="16" height="84" fill="#d97706" />
        <path d="M384 280 L 392 306 L 400 280 Z" fill="#f5d0a9" />
        <path d="M389 296 L 392 306 L 395 296 Z" fill="#181a3d" />
        <rect x="384" y="188" width="16" height="10" fill="#5b57e8" />
      </g>
      {/* small stars */}
      <g fill="#5b57e8">
        <path d="M96 84 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4 z" />
        <path d="M420 150 l3 8 8 3 -8 3 -3 8 -3 -8 -8 -3 8 -3 z" opacity="0.7" />
      </g>
    </svg>
  )
}
