# BibleAgent MCP Service (x402 Payments)

An AI Bible study agent monetized via x402 cryptocurrency payments.

## Features

- **Bible Verse Search** - Search any verse in 4 translations
- **Word Mentions** - Find all verses mentioning a concept
- **Cross-References** - Connect passages between books
- **Strong's Concordance** - Morphological analysis of biblical words
- **Payment Gating** - x402 USDC payments via Base network

## MCP Tools

| Tool | Description | Price |
|------|-------------|-------|
| `search-verse` | Find exact verse text | $0.005 USDC |
| `find-mentions` | Search word/concept across Bible | $0.005 USDC |
| `cross-reference` | Compare two passages | $0.010 USDC |
| `strongs-word` | Strong's Concordance lookup | $0.005 USDC |

## Quick Start

```bash
# Install dependencies
npm install

# Run in development
npm run dev

# Start production
npm start

# Deploy to x402
npm run deploy
```

## x402 Configuration

- Network: Base (eip155:8453)
- Token: USDC
- Wallet: Set via X402_WALLET env var
- Facilitator: https://facilitator.x402.dev

## License

Proprietary - All rights reserved.
