# Code Reading Strategies

Quick strategies for understanding unfamiliar codebases efficiently.

## Reading Order Priority

### 1. Start with Documentation
- `README.md` - Project overview, setup, usage
- `CONTRIBUTING.md` - Development guidelines
- `/docs` folder - Architecture decisions, API docs
- Inline code comments for complex logic

### 2. Configuration Files (reveals dependencies and setup)
- Dependencies show what frameworks/libraries are used
- Scripts show common development tasks
- Environment variables show external integrations

### 3. Entry Points (find where execution begins)
- Main files: `main.py`, `index.js`, `app.js`, `server.js`
- For web apps, follow the routing setup
- For CLIs, check the argument parser

### 4. Routes/Controllers (understand the API surface)
- Shows all endpoints and their handlers
- Reveals the application's capabilities
- Entry point into business logic

### 5. Models/Schemas (understand the data)
- Core entities in the system
- Relationships between entities
- Validation rules and constraints

### 6. Core Business Logic
- Services, use cases, domain logic
- The "what" and "why" of the application
- Usually the most complex code

## Framework-Specific Reading Paths

### React Application
1. `package.json` - Dependencies (React, Next.js, state management)
2. `src/index.js` or `pages/_app.js` - Root component
3. `src/App.js` - Main component, routing setup
4. `/components` - UI building blocks
5. `/pages` or `/routes` - Screen-level components
6. State management files (`/store`, `/context`)

### Express.js API
1. `package.json` - Dependencies
2. `server.js` or `app.js` - Server setup, middleware
3. `/routes` - API endpoints
4. `/controllers` - Request handlers
5. `/models` - Database schemas
6. `/middleware` - Auth, validation, etc.

### Django Project
1. `requirements.txt` - Dependencies
2. `settings.py` - Configuration
3. `urls.py` - URL routing
4. `models.py` - Database models
5. `views.py` - Request handlers
6. `serializers.py` - API data formatting (if DRF)

### Next.js Application
1. `package.json` - Dependencies
2. `next.config.js` - Framework config
3. `/pages` or `/app` - File-based routing
4. `/components` - Reusable components
5. `/api` folder - API routes
6. `/lib` or `/utils` - Shared logic

## Code Pattern Recognition

### Identifying Layers by Imports

**Frontend Component** (imports UI libraries):
```javascript
import React from 'react';
import { Button } from '@/components/ui';
import { useUser } from '@/hooks/useUser';
```

**Backend Route Handler** (imports business logic):
```javascript
import { UserService } from '@/services/user';
import { authenticate } from '@/middleware/auth';
```

**Data Model** (imports ORM):
```python
from django.db import models
from sqlalchemy import Column, String, Integer
```

**Service/Business Logic** (imports models, external APIs):
```javascript
import { User } from '@/models/user';
import axios from 'axios';
```

### Common Code Smells to Notice

**Long files** (>500 lines)
- Likely doing too much, should be split
- Focus on understanding the main responsibilities first

**Deep nesting** (>3 levels)
- Complex conditional logic
- May need refactoring, but understand intent first

**Many imports** (>15)
- File has high coupling
- Central/important file or needs refactoring

**No tests**
- Proceed carefully, logic may be fragile
- High risk of breaking things

## Quick Understanding Techniques

### 1. Search for Key Terms
- `grep -r "class.*Controller"` - Find all controllers
- `grep -r "def.*test_"` - Find all tests
- `grep -r "TODO\|FIXME"` - Known issues
- `grep -r "authenticate\|authorize"` - Auth logic

### 2. Trace a Single Feature End-to-End
Pick one feature (e.g., "user login"), then:
1. Find the UI component that triggers it
2. Follow the API call
3. Find the route handler
4. Trace to the service/business logic
5. See how data is persisted

### 3. Check Git History for Context
```bash
git log --oneline --graph
git log --follow <filepath>  # History of a specific file
git blame <filepath>         # Who changed what and when
```

### 4. Use IDE Navigation
- "Go to definition" - Understand function/class origins
- "Find references" - See where something is used
- "File structure" - Quick overview of classes/functions
- "Call hierarchy" - Understand function dependencies

## Understanding Dependencies

### Frontend Dependencies
- **react**, **vue**, **angular** - UI framework
- **next**, **nuxt** - Full-stack framework
- **redux**, **mobx**, **zustand** - State management
- **react-query**, **swr** - Data fetching
- **axios**, **fetch** - HTTP client
- **tailwindcss**, **styled-components** - Styling
- **react-router** - Client-side routing
- **formik**, **react-hook-form** - Form handling

### Backend Dependencies
- **express**, **fastify**, **koa** - Node.js web framework
- **django**, **flask**, **fastapi** - Python web framework
- **spring-boot** - Java web framework
- **sequelize**, **typeorm**, **prisma** - Node.js ORM
- **sqlalchemy** - Python ORM
- **passport**, **jsonwebtoken** - Authentication
- **joi**, **yup**, **zod** - Validation
- **winston**, **pino** - Logging
- **jest**, **mocha**, **pytest** - Testing

### Database Libraries
- **pg**, **mysql2** - Database drivers
- **mongodb**, **mongoose** - MongoDB
- **redis** - Caching
- **elasticsearch** - Search engine

## Reading Complex Code

### State Machines
Look for:
- Enums or constants defining states
- Switch statements or if-else chains
- State transition diagrams in comments

### Async/Promise Chains
- Follow data flow through `.then()` or `await`
- Check error handling (`.catch()`, try/catch)
- Look for race conditions in parallel operations

### Event-Driven Code
- Event emitters, listeners, subscribers
- `addEventListener`, `on()`, `subscribe()`
- Message queues (RabbitMQ, Kafka, Redis pub/sub)

### Recursive Functions
- Identify base case (termination condition)
- Understand the recursive step
- Check for depth limits or stack overflow protection

## Anti-Patterns to Recognize

- **God Object**: One class/file doing everything
- **Spaghetti Code**: No clear structure, random dependencies
- **Dead Code**: Commented out code, unused functions
- **Magic Numbers**: Hardcoded values with no explanation
- **Tight Coupling**: Changes in one place break many others
- **No Error Handling**: Assumes happy path always works

## Questions to Answer When Reading Code

1. **What problem does this solve?**
2. **What are the inputs and outputs?**
3. **What are the side effects?** (DB writes, API calls, file I/O)
4. **What can go wrong?** (Edge cases, errors)
5. **How is this tested?**
6. **Why was it implemented this way?** (Check comments, commits, docs)
7. **How does this integrate with the rest of the system?**
