/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "aurora": {
          "from": {
            backgroundPosition: "50% 50%, 50% 50%",
          },
          "to": {
            backgroundPosition: "350% 50%, 350% 50%",
          },
        },
        "float": {
          "0%, 100%": {
            transform: "translateY(0px) translateX(0px)",
            opacity: "0.6",
          },
          "25%": {
            transform: "translateY(-10px) translateX(5px)",
            opacity: "1",
          },
          "50%": {
            transform: "translateY(-5px) translateX(-5px)",
            opacity: "0.8",
          },
          "75%": {
            transform: "translateY(-15px) translateX(3px)",
            opacity: "0.9",
          },
        },
        "spin-slow": {
          "from": {
            transform: "rotate(0deg)",
          },
          "to": {
            transform: "rotate(360deg)",
          },
        },
        "spin-reverse": {
          "from": {
            transform: "rotate(360deg)",
          },
          "to": {
            transform: "rotate(0deg)",
          },
        },
        "gradient-shift": {
          "0%, 100%": {
            backgroundPosition: "0% 50%",
          },
          "50%": {
            backgroundPosition: "100% 50%",
          },
        },
        "shimmer": {
          "0%": {
            backgroundPosition: "-200% 0",
          },
          "100%": {
            backgroundPosition: "200% 0",
          },
        },
        "chart-draw": {
          "0%": {
            strokeDasharray: "0 1000",
            strokeDashoffset: "0",
          },
          "100%": {
            strokeDasharray: "1000 0",
            strokeDashoffset: "0",
          },
        },
        "chart-pulse": {
          "0%, 100%": {
            opacity: "0.6",
            transform: "scale(1)",
          },
          "50%": {
            opacity: "1",
            transform: "scale(1.05)",
          },
        },
        "bounce-gentle": {
          "0%, 100%": {
            transform: "translateY(0)",
          },
          "50%": {
            transform: "translateY(-10px)",
          },
        },
        "glow-pulse": {
          "0%, 100%": {
            boxShadow: "0 0 20px rgba(255, 255, 255, 0.3)",
          },
          "50%": {
            boxShadow: "0 0 40px rgba(255, 255, 255, 0.6)",
          },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "aurora": "aurora 60s linear infinite",
        "float": "float 6s ease-in-out infinite",
        "spin-slow": "spin-slow 20s linear infinite",
        "spin-reverse": "spin-reverse 15s linear infinite",
        "gradient-shift": "gradient-shift 8s ease-in-out infinite",
        "shimmer": "shimmer 3s ease-in-out infinite",
        "chart-draw": "chart-draw 4s ease-out forwards",
        "chart-pulse": "chart-pulse 2s ease-in-out infinite",
        "bounce-gentle": "bounce-gentle 3s ease-in-out infinite",
        "glow-pulse": "glow-pulse 2s ease-in-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

