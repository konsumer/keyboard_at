This will let you use the web to view the clock/data pins on your keyboard.

## install

```sh
ampy --port ${PORT} put plot.py
```

Now, go [here](https://keebplot.surge.sh).


## development

local-dev requires https, so I made a lil server:

```
./server.py
```

I deploy like this:

```
npx -y surge webroot keebplot.surge.sh
```
