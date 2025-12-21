Entities:
    User
    Project
    Task

    User(django default):
        id(pk)
        name
        email
        password
        info

    Project:
        id(pk)
        name
        description
        owner(fk -> user)
        created_at
        expected_end_date

    Task:
        id
        title
        description
        status(todo, in_progress, done)
        project(fk -> ptoject)
        assigned_to(fk -> user)
        created_by(fk -> user)
        created_at
