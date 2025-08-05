# Copilot Code Quality Instructions

## Core Principles

Follow software engineering fundamentals for maintainable, scalable code.

## SOLID Principles

**Single Responsibility**: Each class/function should have one reason to change. Focus on single, well-defined purposes.

**Open/Closed**: Design for extension without modification. Use abstractions and interfaces.

**Liskov Substitution**: Subtypes must be substitutable for their base types without breaking functionality.

**Interface Segregation**: Create focused, specific interfaces rather than large, general ones.

**Dependency Inversion**: Depend on abstractions, not concrete implementations. Use dependency injection.

## Design Principles

**DRY (Don't Repeat Yourself)**: Extract common functionality into reusable components.

**KISS (Keep It Simple)**: Choose the simplest solution that meets requirements. Avoid over-engineering.

**YAGNI (You Aren't Gonna Need It)**: Don't implement features until they're actually needed.

## Code Quality Guidelines

- Write self-documenting code with meaningful names
- Prioritize readability over cleverness
- Handle errors gracefully with appropriate exception handling
- Use consistent naming conventions and formatting
- Minimize function/method complexity and cognitive load
- Favor composition over inheritance
- Apply defensive programming practices

## Testing & Documentation

- Write testable code with clear boundaries
- Include comprehensive error handling
- Document public APIs and complex business logic
- Consider edge cases and input validation

## Performance & Security

- Optimize after profiling, not prematurely
- Follow security best practices for data handling
- Use appropriate data structures and algorithms
- Consider scalability implications in design decisions
