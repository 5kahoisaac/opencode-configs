---
name: "mnemonics"
description: "Mnemonics skill provides intelligent memory management with architectural decision tracking, design pattern storage, and learning accumulation. Integrates with oh-my-opencode orchestration for automatic recall, manual remember/forget triggers, and circular memory references to create adaptive knowledge systems."
---

# Mnemonics Skill

## Memory Operations

### memory_remember
Stores new memories using hybrid classification combining content analysis, semantic similarity, and contextual clustering. Automatically categorizes memories as architectural decisions, design patterns, learning insights, or general knowledge. Creates linked references between related memories.

**Usage:**
- New memories trigger automatic classification and clustering
- Similarity detection identifies existing related memories
- Creates bidirectional references for knowledge discovery
- Persistent storage with automated recall triggers

### memory_recall
Retrieves memories using multi-criteria search including semantic similarity, temporal proximity, and relevance scoring. Supports automatic recall via oh-my-opencode orchestration during code analysis, agent operations, and skill execution.

**Usage:**
- Context-aware retrieval based on current task
- Fuzzy matching with agent-based similarity algorithms
- Automatic recall during workflow execution
- Manual search by memory type or keywords

### memory_forget
Performs selective memory removal with dependency analysis. Prevents deletion of memories that are referenced by other memories, maintaining knowledge integrity. Supports bulk operations and pattern-based forgetting.

**Usage:**
- Safe deletion with reference validation
- Bulk operations for memory lifecycle management
- Pattern-based forgetting (e.g., time-based, relevance-based)
- Maintains memory system integrity

## Resource References

### Templates
- `templates/response/memory-template.md`: Standard memory format with structured metadata
- `templates/response/decision-template.md`: Architectural decision template
- `templates/response/pattern-template.md`: Design pattern template

### Scripts
- `scripts/memory-classifier.py`: Hybrid classification engine
- `scripts/similarity-detector.py`: Agent-based similarity scoring
- `scripts/memory-graph.py`: Linked reference maintenance
- `scripts/auto-recall.py`: Automatic recall integration

## Algorithm Features

### Hybrid Classification Approach
Combines multiple classification methods for robust memory categorization:
1. **Content Analysis**: Extracts key concepts and technical vocabulary
2. **Contextual Clustering**: Groups memories by project and task context
3. **Semantic Similarity**: Uses embeddings to identify related content
4. **User Feedback**: Learns from agent usage patterns

### Agent-Based Similarity Detection
Employs specialized agents for memory matching:
1. **Semantic Agent**: Analyzes conceptual similarity using embeddings
2. **Temporal Agent**: Considers time proximity and project context
3. **Structural Agent**: Examines code patterns and architectural elements
4. **Hybrid Scoring**: Combines all agents for weighted relevance

### Linked Memory References
Creates bidirectional knowledge networks:
1. **Automatic Linking**: Identifies and connects related memories
2. **Circular References**: Supports circular dependencies for complex knowledge
3. **Reference Tracking**: Maintains memory dependency graphs
4. **Network Navigation**: Enables discovery through linked connections

## Memory Examples

```yaml
# Good Memory Example 1: Architectural Decision
type: architectural_decision
content: "Uses Bun runtime for faster script execution in build pipeline"
created: 2025-06-15
tags: ["performance", "build-system", "javascript"]
references: []
```

```yaml
# Good Memory Example 2: Design Pattern  
type: design_pattern
content: "Never use \`any\` type in TypeScript - specific types prevent runtime errors"
created: 2025-06-20
tags: ["typescript", "type-safety", "best-practices"]
references: []
```

```yaml
# Good Memory Example 3: Learning
type: learning
content: "Serena tools reduce token consumption 60% compared to grep operations"
created: 2025-06-22
tags: ["performance", "optimization", "tools"]
references: []
```

```yaml
# Good Memory Example 4: Architectural Decision
type: architectural_decision
content: "Skills directory structure follows OhMyOpenCode conventions for easy discovery"
created: 2025-06-25
tags: ["organization", "conventions", "structure"]
references: []
```

```yaml
# Good Memory Example 5: Design Pattern
type: design_pattern
content: "Use YAML frontmatter for skills - enables metadata extraction and validation"
created: 2025-06-28
tags: ["formatting", "metadata", "best-practices"]
references: []
```

## Error Handling Behaviors

### Memory Creation Errors
- **Validation Failures**: Reject memories without required metadata
- **Classification Errors**: Log warnings and fall back to general category
- **Reference Conflicts**: Resolve circular dependencies automatically

### Recall System Errors
- **Search Failures**: Return empty results with error logging
- **Timeout Handling**: Implement graceful degradation for slow searches
- **Memory Corruption**: Auto-repair reference graphs when detected

### Forgetting Operations
- **Dependency Violations**: Prevent deletion of referenced memories
- **Batch Failures**: Continue with remaining operations on partial failures
- **Permission Errors**: Log and skip unauthorized access attempts

## Integration Features

### Oh-My-OpenCode Orchestration
- **Automatic Recall**: Triggers memory retrieval during agent operations
- **Context Integration**: Uses task context to enhance memory relevance
- **Skill Coordination**: Coordinates memory operations across skills
- **Persistent Storage**: Maintains memories across sessions

### Manual Triggers
- **Agent Commands**: Direct remember/forget through agent interfaces
- **File Analysis**: Automatic memory creation during file processing
- **Pattern Matching**: Trigger based on content similarity
- **Time-Based**: Automatic cleanup of outdated memories

The mnemonics skill creates an intelligent memory system that learns from agent interactions and provides context-aware knowledge management for enhanced decision-making and learning.