# Common Software Architecture Patterns Reference

This document provides quick reference for understanding common software project architectures, layers, and organizational patterns.

## Common Project Layers

### Frontend Projects

**Components Layer** (`/components`, `/src/components`)
- Reusable UI elements (buttons, forms, cards)
- Often split into atomic/presentational vs container/smart components
- Purpose: Modular, testable UI building blocks

**Pages/Views Layer** (`/pages`, `/views`, `/src/pages`)
- Route-level components that compose smaller components
- Each file typically corresponds to a URL route
- Purpose: Define application screens and navigation structure

**State Management** (`/store`, `/redux`, `/state`, `/context`)
- Global application state (user session, app config, cached data)
- Common libraries: Redux, MobX, Zustand, Context API
- Purpose: Share data across components without prop drilling

**Utilities/Helpers** (`/utils`, `/helpers`, `/lib`)
- Shared functions, formatters, validators
- Business logic that doesn't belong in components
- Purpose: DRY principle, reusable logic

**Assets/Static** (`/assets`, `/public`, `/static`)
- Images, fonts, icons, static files
- Served directly without processing
- Purpose: Non-code resources

### Backend Projects

**Routes/Controllers Layer** (`/routes`, `/controllers`, `/api`)
- HTTP endpoint definitions
- Maps URLs to business logic functions
- Purpose: API interface, request handling

**Services/Business Logic** (`/services`, `/business`, `/domain`)
- Core application logic, complex operations
- Independent of HTTP layer
- Purpose: Reusable business rules, domain logic

**Models/Entities** (`/models`, `/entities`, `/schemas`)
- Data structures, database schemas
- ORM models (Sequelize, TypeORM, SQLAlchemy, etc.)
- Purpose: Define data shape and relationships

**Middleware** (`/middleware`, `/middlewares`)
- Request interceptors (auth, logging, validation)
- Execute before route handlers
- Purpose: Cross-cutting concerns

**Data Access Layer** (`/repositories`, `/dao`, `/data`)
- Database query abstraction
- Separates business logic from data persistence
- Purpose: Encapsulate database operations

**Configuration** (`/config`, `/settings`)
- App configuration, environment-specific settings
- Database connections, API keys, feature flags
- Purpose: Centralize configuration

### Full-Stack/Monorepo Projects

**Apps/Packages Structure**
```
/apps
  /web          - Frontend application
  /api          - Backend API
  /mobile       - Mobile app
/packages
  /shared       - Shared code
  /ui           - Shared components
  /types        - Shared TypeScript types
```

## Common Architecture Patterns

### MVC (Model-View-Controller)
- **Model**: Data and business logic
- **View**: User interface
- **Controller**: Handles requests, coordinates model and view
- Found in: Rails, Django, Laravel, ASP.NET MVC

### Layered/N-Tier Architecture
- **Presentation**: UI layer
- **Business Logic**: Application logic
- **Data Access**: Database operations
- **Database**: Data storage
- Clear separation of concerns, each layer only talks to adjacent layers

### Microservices
```
/services
  /user-service
  /order-service
  /payment-service
```
- Independent, deployable services
- Each service owns its data
- Communicate via APIs or message queues

### Clean/Hexagonal Architecture
```
/domain         - Core business logic (no dependencies)
/application    - Use cases, orchestration
/infrastructure - External concerns (DB, HTTP, etc.)
/interfaces     - Adapters (REST, GraphQL, CLI)
```
- Business logic at center, independent of frameworks
- Dependencies point inward

## Project Type Indicators

### React/Next.js
- `package.json` with react/next dependencies
- `pages/` or `app/` directory (Next.js)
- `.jsx` or `.tsx` files
- `next.config.js`

### Vue.js
- `package.json` with vue dependency
- `.vue` single-file components
- `vue.config.js`

### Node.js/Express API
- `package.json` with express
- Route files in `/routes` or `/api`
- Typically `server.js` or `app.js` entry point

### Python/Django
- `manage.py` file
- `settings.py` configuration
- App structure with `/models.py`, `/views.py`, `/urls.py`

### Python/Flask
- `app.py` or `wsgi.py`
- Lightweight structure, more flexible than Django

### Go
- `go.mod` for dependencies
- `main.go` entry point
- Package-based organization

### Rust
- `Cargo.toml` for dependencies
- `src/main.rs` or `src/lib.rs`
- `target/` for build artifacts

### Java/Spring
- `pom.xml` (Maven) or `build.gradle` (Gradle)
- Package structure: `com.company.project`
- Annotations: `@Controller`, `@Service`, `@Repository`

## Key Configuration Files

### Dependency Management
- `package.json` - Node.js
- `requirements.txt`, `pyproject.toml` - Python
- `Gemfile` - Ruby
- `Cargo.toml` - Rust
- `go.mod` - Go
- `pom.xml`, `build.gradle` - Java

### Build/Bundler
- `webpack.config.js` - Webpack
- `vite.config.js` - Vite
- `tsconfig.json` - TypeScript
- `babel.config.js` - Babel

### Environment
- `.env` - Environment variables (secrets, config)
- `.env.example` - Template for required variables

### Testing
- `jest.config.js` - Jest (JavaScript)
- `pytest.ini` - Pytest (Python)
- `karma.conf.js` - Karma
- Test files often in `/tests` or `/test` or colocated with `*.test.js`

### Code Quality
- `.eslintrc` - ESLint linting rules
- `.prettierrc` - Prettier formatting
- `tslint.json` - TSLint (legacy)
- `pyproject.toml` - Python tooling (Black, isort, etc.)

### Docker
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container orchestration

### CI/CD
- `.github/workflows/` - GitHub Actions
- `.gitlab-ci.yml` - GitLab CI
- `Jenkinsfile` - Jenkins
- `.circleci/config.yml` - CircleCI
