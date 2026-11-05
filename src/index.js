import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "BibleAgent",
  version: "1.0.0",
  description: "AI Bible study agent with payment gating via x402. Access indexed Bible translations, Strong's concordance, and cross-references."
});

server.tool(
  "search-verse",
  "Search any verse in the Bible and return the text with Strong's reference",
  {
    book: z.string().describe("Book name (e.g., 'John')"),
    chapter: z.number().min(1).max(150).describe("Chapter number"),
    verse: z.number().min(1).max(2000).describe("Verse number"),
    translation: z.enum(["pdt", "sv1888", "kjv", "sl2000"]).default("pdt").describe("Translation to use")
  },
  async ({ book, chapter, verse, translation }) => {
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          book: book.charAt(0).toUpperCase() + book.slice(1).toLowerCase(),
          chapter,
          verse,
          translation,
          message: `Verse ${book} ${chapter}:${verse} would be retrieved from the database.`
        })
      }]
    };
  }
);

server.tool(
  "find-mentions",
  "Find all verses mentioning a specific word or concept with Strong's root analysis",
  {
    term: z.string().min(2).describe("Word or concept to search for"),
    translation: z.enum(["pdt", "sv1888", "kjv", "sl2000"]).default("pdt").describe("Translation to use")
  },
  async ({ term, translation }) => {
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          term,
          translation,
          results: `Will search for mentions of '${term}' in ${translation} translation.`
        })
      }]
    };
  }
);

server.tool(
  "cross-reference",
  "Find cross-references between two Bible passages",
  {
    passage1: z.string().describe("First passage (e.g., 'John 3:16')"),
    passage2: z.string().describe("Second passage (e.g., 'Romans 8:28')"),
    translation: z.enum(["pdt", "sv1888", "kjv", "sl2000"]).default("pdt").describe("Translation to use")
  },
  async ({ passage1, passage2, translation }) => {
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          passage1,
          passage2,
          translation,
          results: `Cross-reference analysis for ${passage1} and ${passage2} in ${translation}.`
        })
      }]
    };
  }
);

server.tool(
  "strongs-word",
  "Get Strong's Concordance entry for a word with morphological analysis",
  {
    word: z.string().min(2).describe("Word to look up in Strong's Concordance"),
    translation: z.enum(["pdt", "sv1888", "kjv", "sl2000"]).default("pdt").describe("Translation to use")
  },
  async ({ word, translation }) => {
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          word,
          translation,
          result: `Strong's Concordance entry for '${word}' in ${translation}.`
        })
      }]
    };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
