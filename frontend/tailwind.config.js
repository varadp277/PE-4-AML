/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        cyber: {
          darkest: '#070b14',
          darker: '#0b1324',
          card: '#0f1c34',
          cardHover: '#142545',
          border: '#1e3256',
          teal: '#0df2c9',
          tealDark: '#089981',
          cyan: '#38bdf8',
          blue: '#2563eb',
          amber: '#f59e0b',
          rose: '#f43f5e',
          textMuted: '#94a3b8',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
      },
      boxShadow: {
        'glow-teal': '0 0 20px -3px rgba(13, 242, 201, 0.3)',
        'glow-cyan': '0 0 20px -3px rgba(56, 189, 248, 0.3)',
        'glow-rose': '0 0 20px -3px rgba(244, 63, 94, 0.35)',
        'cyber-card': '0 4px 20px -2px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(30, 50, 86, 0.5)',
      }
    },
  },
  plugins: [],
}
