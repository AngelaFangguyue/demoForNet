### Require

1. node.js
2. python
3. virtualenv



### Install

##### Step 1.

```
cd project
virtualenv --no-site-packages venv

venv\Scripts\activate	# for Windows
. venv/bin/activate		# for Unix
	
pip install -r requirements.txt
```



##### Step 2.

```
cd frontend
npm install
```



### Build

```
cd frontend

npm start		# for dev
npm run build	# for production
```