# Python_flask


## bash Commands

Running program
bash ```
    export FLASK_APP=filename.py
    flask run
```
Above command will not implement every changes, to do so you need to run this command after every changes to see change.
Alternative way to do so is 

bash ```
    export FLASK_DEBUG=1
    flask run
```
In this it will monitor each changes and implement in output.

One more way 

This should be in py file

python```
    if __name__ == "__main__":
        name.run(debug=True)
```
and command is 

bash```
    python filename.py
```