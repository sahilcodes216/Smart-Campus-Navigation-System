/**
 * Search & Directory Engine
 * Conforms to PRD Section 6.3 & Acceptance Criteria
 */

export class CampusSearch {
  constructor(locations = [], categories = []) {
    this.locations = locations;
    this.categories = categories;
  }

  /**
   * Simple fuzzy match checking if pattern characters occur in target in sequence
   * with minor typo tolerance
   */
  fuzzyMatch(target = '', query = '') {
    if (!target || !query) return { match: false, score: 0 };
    const t = target.toLowerCase();
    const q = query.toLowerCase().trim();

    // Exact substring match (highest priority)
    const exactIndex = t.indexOf(q);
    if (exactIndex !== -1) {
      return { match: true, score: 100 - exactIndex, index: exactIndex, len: q.length };
    }

    // Word prefix match
    const words = t.split(/[\s,/-]+/);
    for (const w of words) {
      if (w.startsWith(q)) {
        return { match: true, score: 80, index: t.indexOf(w), len: q.length };
      }
    }

    // Subsequence fuzzy match
    let qIdx = 0;
    let matches = 0;
    for (let i = 0; i < t.length && qIdx < q.length; i++) {
      if (t[i] === q[qIdx]) {
        matches++;
        qIdx++;
      }
    }

    if (qIdx === q.length && q.length >= 2) {
      return { match: true, score: 50 + matches, index: -1, len: 0 };
    }

    // Levenshtein / 1-transposition tolerance for words >= 4 chars
    if (q.length >= 4) {
      for (const w of words) {
        if (Math.abs(w.length - q.length) <= 1) {
          let diffs = 0;
          for (let k = 0; k < Math.min(w.length, q.length); k++) {
            if (w[k] !== q[k]) diffs++;
          }
          if (diffs <= 1) {
            return { match: true, score: 40, index: t.indexOf(w), len: w.length };
          }
        }
      }
    }

    return { match: false, score: 0 };
  }

  /**
   * Search against name, aliases, category, building, and landmarks
   */
  search(query = '', selectedCategories = [], sortBy = 'name') {
    let results = [...this.locations];

    // Filter by categories (multi-select)
    if (selectedCategories && selectedCategories.length > 0) {
      results = results.filter(loc => selectedCategories.includes(loc.category));
    }

    const cleanQuery = query.trim();
    if (cleanQuery) {
      const scoredResults = [];
      for (const loc of results) {
        let bestMatch = { match: false, score: 0, field: '', matchInfo: null };

        // 1. Match Name
        const nameMatch = this.fuzzyMatch(loc.name, cleanQuery);
        if (nameMatch.match && nameMatch.score + 50 > bestMatch.score) {
          bestMatch = { match: true, score: nameMatch.score + 50, field: 'name', matchInfo: nameMatch };
        }

        // 2. Match Building
        const bldgMatch = this.fuzzyMatch(loc.building, cleanQuery);
        if (bldgMatch.match && bldgMatch.score + 30 > bestMatch.score) {
          bestMatch = { match: true, score: bldgMatch.score + 30, field: 'building', matchInfo: bldgMatch };
        }

        // 3. Match Aliases
        if (Array.isArray(loc.aliases)) {
          for (const alias of loc.aliases) {
            const aliasMatch = this.fuzzyMatch(alias, cleanQuery);
            if (aliasMatch.match && aliasMatch.score + 25 > bestMatch.score) {
              bestMatch = { match: true, score: aliasMatch.score + 25, field: 'alias', matchInfo: aliasMatch };
            }
          }
        }

        // 4. Match Category
        const catMatch = this.fuzzyMatch(loc.category, cleanQuery);
        if (catMatch.match && catMatch.score + 20 > bestMatch.score) {
          bestMatch = { match: true, score: catMatch.score + 20, field: 'category', matchInfo: catMatch };
        }

        // 5. Match Description & Landmarks
        const descMatch = this.fuzzyMatch(loc.description, cleanQuery);
        if (descMatch.match && descMatch.score + 10 > bestMatch.score) {
          bestMatch = { match: true, score: descMatch.score + 10, field: 'description', matchInfo: descMatch };
        }

        if (bestMatch.match) {
          scoredResults.push({
            location: loc,
            score: bestMatch.score,
            bestField: bestMatch.field,
            matchInfo: bestMatch.matchInfo
          });
        }
      }

      // Sort by search score descending
      scoredResults.sort((a, b) => b.score - a.score);
      results = scoredResults.map(item => item.location);
    } else {
      // Sort standard
      if (sortBy === 'name') {
        results.sort((a, b) => a.name.localeCompare(b.name));
      } else if (sortBy === 'category') {
        results.sort((a, b) => a.category.localeCompare(b.category) || a.name.localeCompare(b.name));
      } else if (sortBy === 'building') {
        results.sort((a, b) => a.building.localeCompare(b.building));
      }
    }

    return results;
  }

  /**
   * Helper to safely highlight matched substring with <mark class="search-highlight">
   */
  static highlight(text = '', query = '') {
    if (!text || !query.trim()) return text;
    const escaped = query.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escaped})`, 'gi');
    return text.replace(regex, '<mark class="search-highlight">$1</mark>');
  }
}
