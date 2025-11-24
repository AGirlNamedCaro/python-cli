# Architecture Decision Record

## Project: Safe File Operations Toolkit

This document explains key design decisions made during the development of this project.

## Table of Contents
1. [Architecture & Project Structure](#1-architecture--project-structure)
2. [Security Model](#2-security-model)
3. [Error Handling Strategy](#3-error-handling-strategy)
4. [Command Design Patterns](#4-command-design-patterns)

## 1. Architecture & Project Structure
* <b>Separation of Concerns: </b>
    * This project was built with 4 layers in mind in:
        * SafeFileSystem
            * Path validation & safe file operations
        * Commands
            * Business logic for specific operations
        * Router:
            * Command dispatch logic
        * CLI
            * Argument parsing and user interaction

    * This ensures that each layer only has a <i>single</i> responsibility
    * This makes the project easier to follow, easier to test, and I can potentially reuse the SafeFileSystem without changing it
    * A <i>Monolithic</i> <code>cli.py</code> with all the logic would become unmaintainable with 5+ commands
    * <b>Tradeoff: </b>
        * <b>Cost: </b> More files, more structure
        * <b>Benefit: </b> Each piece is simple, testable, reusable
* <b>Dependency Direction: </b>
    * Dependencies flow downward (CLI -> Commands -> FileSystem)
    * Dependencies should flow in one direction <b>(Dependency Inversion Principle)</b> in order to avoid tight coupling between modules (i.e you can't change one without potentially breaking the other), increasing complexity, and reducing reusability. 

* <b>Testability: </b> Each layer can be tested in isolation

    
## 2. Security Model
* Every <code>SafeFileSystem</code> instance has a root directory because all operations are restricted within this boundary.
    * This only allows access to necessary files
    * Prevents <i>Path traversal attacks</i>
        * Converts paths to absolute with <code>resolve()</code>
        * Verifies that the result is within root
        * Rejects if outside of boundary
    * <b>Tradeoff: </b>
        * <b>Cost: </b>
            * Extra validation on every file operation
        * <b>Benefit: </b>
            * Prevents a security breach
    * <b>Blocking <i>all</i> Symlinks:</b>
        *  Symlinks are forebidden by default even if they point to the root
            * This makes the system less flexible but more secure
        * <b>Tradeoff: </b>
            * <b>Cost: </b>
                * Less flexibility
                * Rejected the idea of allowing symlinks if they resolve within root because it was more complex and it could potentially allow for race condition risks
            * <b>Benefits: </b>
                * More secure.( Avoids Time of Check, Time of Use attacks)
            * Future Update:
                * Will consider adding a configurable flag that will allow users to allow symlinks if they resolve within root. Will need to figure out how to handle race condition risks
    * <b>Validation at <i>every</i> entry point </b>
        * Every <code>SafeFileSystem</code> method validates paths, even when the caller has already validated.
        * I wanted to implement a <i>defense in depth</i> strategy, where there are multiple levels of security. If someone adds new code that perhaps bypasses one validation layer, the other layerse still protect us. Each method is independently safe.
        * <b>TradeOff</b>
            * <b>Cost: </b>
                * Performance overhead
            * <b>Benefit: </b>
                * Prevents bugs from new code
## 3. Error Handling Strategy
* <b>Custom exceptions for doman errors</b>
    * Increases clarity: excpetion name explains what went wrong
    * Specific
    * Can provide context-specific error messages
* I considered using built-in excpetions only but felt like it didn't provide the user enough context in certain instances for what went wrong

## 4. Command Design Patterns
* Commands return formatted strings, they don't print directly
    * Did this with separation of concerns in mind
        * Commands handle logic while the CLI handles the presentation
    * Easier to test
    * <b>Tradeoff: </b>
        * <b>Cost: </b>
            * More code
        * <b> Benefit: </b>
            * Reusable in any context
            * Easy to test
* Commands receive <code>SafeFileSystem</code> instance as a parameter rather than creating their own
    * Easier to test
    * Flexible, as different callers can provide different roots
    * Dependency Injection is a well-known design pattern
* Dry-Run Pattern for destructive operations
    * The <code>replace</code> defaults to a dry-run (preview) that requires an explicit <code> --appluy</code> flag to modify the files
    * This makes this command <i>safe by default</i> and prevents accidental data loss
    * Industry standard
    * Increases user confidence by allowing users to preview their changes before comitting
* <b>Tradeoff: </b>
    * <b>Cost: </b>
        * Users have to add the <code>--apply</code> flag
    * <b>Benefit: </b>
        * Prevents accidental data loss