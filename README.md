# Configfy
Decorator library to configure function arguments
by manuel.pasieka@protonmail.ch

## Example usage
Running example.py

```bash
> python example.py

# Use default config.ini file (missing greetings section)...
Hello Bob, I am Suzan Flusan!
WARNING:root:Config section greetings_section not found!
Hello Tom! How are you doing?
Goodby!

# Changing config to "another_config.ini" ...
Hello Bob, I am Pedro!
Hallo Tom! Wie gehts?
Goodby!

# Specifying kwargs, overwriting config settings...
Hello Bob, I am Alfredo!
Zdravo Tom! Kako si?
That's all Folks!

Comparing performance ... this can take a while.
native: 12.087 sec
configfy 12.213 sec
configfy added 0.00012617137702181935 sec to the function call!
```