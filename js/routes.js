/**
 * Graph Routing Engine & Dijkstra Algorithm
 * Conforms to PRD Section 6.5, 9, 10
 */

export class CampusRouter {
  constructor(nodes = [], edges = []) {
    this.nodes = new Map();
    this.adjacency = new Map();
    this.edges = edges;

    nodes.forEach(node => {
      this.nodes.set(node.id, node);
      this.adjacency.set(node.id, []);
    });

    edges.forEach(edge => {
      if (this.adjacency.has(edge.from) && this.adjacency.has(edge.to)) {
        this.adjacency.get(edge.from).push({
          to: edge.to,
          meters: edge.meters,
          accessible: edge.accessible !== false,
          label: edge.label || 'Campus Path'
        });
        // Undirected walkable edges
        this.adjacency.get(edge.to).push({
          to: edge.from,
          meters: edge.meters,
          accessible: edge.accessible !== false,
          label: edge.label || 'Campus Path'
        });
      }
    });
  }

  /**
   * Calculates the shortest path between startNodeId and endNodeId using Dijkstra's algorithm
   * @param {string} startNodeId 
   * @param {string} endNodeId 
   * @param {boolean} accessibleOnly 
   * @returns {Object} result object containing path, totalMeters, estimatedMinutes, steps, or error
   */
  findRoute(startNodeId, endNodeId, accessibleOnly = false) {
    if (!startNodeId || !endNodeId) {
      return { error: 'MISSING_SELECTION', message: 'Please select both starting point and destination.' };
    }

    if (startNodeId === endNodeId) {
      return { error: 'SAME_LOCATION', message: 'You are already there.' };
    }

    if (!this.nodes.has(startNodeId) || !this.nodes.has(endNodeId)) {
      return { error: 'INVALID_NODE', message: "We can't calculate a route between these two places yet." };
    }

    const distances = new Map();
    const previous = new Map();
    const unvisited = new Set();

    for (const nodeId of this.nodes.keys()) {
      distances.set(nodeId, Infinity);
      unvisited.add(nodeId);
    }

    distances.set(startNodeId, 0);

    while (unvisited.size > 0) {
      // Find node with minimum distance in unvisited set
      let current = null;
      let minDistance = Infinity;

      for (const nodeId of unvisited) {
        const d = distances.get(nodeId);
        if (d < minDistance) {
          minDistance = d;
          current = nodeId;
        }
      }

      if (current === null || minDistance === Infinity) {
        break; // Remaining nodes are unreachable
      }

      if (current === endNodeId) {
        break; // Destination reached
      }

      unvisited.delete(current);

      const neighbors = this.adjacency.get(current) || [];
      for (const neighbor of neighbors) {
        if (!unvisited.has(neighbor.to)) continue;
        if (accessibleOnly && !neighbor.accessible) continue;

        const altDistance = distances.get(current) + neighbor.meters;
        if (altDistance < distances.get(neighbor.to)) {
          distances.set(neighbor.to, altDistance);
          previous.set(neighbor.to, {
            nodeId: current,
            meters: neighbor.meters,
            label: neighbor.label
          });
        }
      }
    }

    if (distances.get(endNodeId) === Infinity) {
      return { error: 'UNREACHABLE', message: "We can't calculate a route between these two places yet." };
    }

    // Reconstruct path
    const pathNodes = [];
    let curr = endNodeId;
    const pathEdges = [];

    while (curr !== startNodeId) {
      pathNodes.unshift(this.nodes.get(curr));
      const step = previous.get(curr);
      if (!step) break;
      pathEdges.unshift(step);
      curr = step.nodeId;
    }
    pathNodes.unshift(this.nodes.get(startNodeId));

    const totalMeters = distances.get(endNodeId);
    // PRD: Estimated walking time is distance divided by 80 m/min
    const estimatedMinutes = Math.max(1, Math.round(totalMeters / 80));

    // Generate human-readable directions (PRD Section 6.5)
    const steps = this.generateStepDirections(pathNodes, pathEdges);

    return {
      success: true,
      startNode: this.nodes.get(startNodeId),
      endNode: this.nodes.get(endNodeId),
      pathNodes,
      totalMeters,
      estimatedMinutes,
      steps
    };
  }

  generateStepDirections(pathNodes, pathEdges) {
    if (pathNodes.length < 2) return [];

    const steps = [];
    const startName = pathNodes[0].name || 'start point';
    const endName = pathNodes[pathNodes.length - 1].name || 'destination';

    // First step
    const firstEdge = pathEdges[0];
    steps.push({
      step: 1,
      instruction: `Depart from ${startName} along ${firstEdge.label || 'the walkway'} (${firstEdge.meters} m).`
    });

    // Intermediate steps
    for (let i = 1; i < pathEdges.length; i++) {
      const edge = pathEdges[i];
      const prevEdge = pathEdges[i - 1];
      const junction = pathNodes[i];
      
      let direction = 'Continue';
      if (edge.label !== prevEdge.label) {
        direction = `Turn onto ${edge.label}`;
      } else {
        direction = `Continue along ${edge.label}`;
      }

      steps.push({
        step: i + 1,
        instruction: `At ${junction.name || 'junction'}, ${direction.toLowerCase()} for ${edge.meters} m.`
      });
    }

    // Arrival step
    steps.push({
      step: steps.length + 1,
      instruction: `Arrive at ${endName}. Your destination will be in front of you.`
    });

    return steps;
  }
}
