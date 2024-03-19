# api-test

This repository contains all the tools for testing and stressing the APIs of the
AI Lab projects.

## Usage

For more detailed information about the usage of Finesse locust tool, please
refer to the [FINESSE_USAGE.md](finesse/FINESSE_USAGE.md) file in the finesse
repository.

## Tools available

There are tools that can integrate with Python or a script to accurately
calculate API statistics. Currently, the needs are to test the tool using JSON
files containing questions and their page origin in order to establish an
accuracy score. We also want to calculate request times and generate a
statistical summary of all this data. That being said, we plan to test the APIs
under different conditions in the near future. For example, with multiple
simultaneous users or under special conditions. That's why it's worth
researching tools, if they are scalable and well adapted with Python.

### Decision

We've opted for Locust as our tool of choice. It's seamlessly compatible with
Python, making it a natural fit due to its easy integration. Locust is an
open-source load testing framework written in Python, designed to simulate
numerous machines sending requests to a given system. It provides detailed
insights into the system's performance and scalability. With its built-in UI and
straightforward integration with Python scripts, Locust is user-friendly and
accessible. It is popular and open source, with support from major tech
companies such as Microsoft and Google

However, Locust's primary purpose is to conduct ongoing tests involving multiple
machines and endpoints simultaneously. Our specific requirement involves running
the accuracy test just once. Nevertheless, there's potential for future
integration, especially for stress and load testing scenarios that involve
repeated searches.

### Alternatives Considered

#### Apache Bench (ab)

Apache Bench (ab) is a command-line tool for benchmarking HTTP servers. It is
included with the Apache HTTP Server package and is designed for simplicity and
ease of use.

Pros

- Simple to use.
- Good for basic testing.
- Easy integration with test scripts.

Cons

- May not be flexible enough for complex testing scenarios.
- Less performant for heavy loads or advanced testing.

#### Siege

Siege is a load testing and benchmarking tool that simulates multiple users
accessing a web server, enabling stress testing and performance evaluation.

Pros

- Supports multiple concurrent users, making it suitable for load testing.
- Allows for stress testing of web servers and applications.

Cons

- Lack of documentation, some arguments are not documented in their wiki.
- May have a steeper learning curve compared to simpler tools like Apache Bench.
