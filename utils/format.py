from subprocess import Popen, PIPE, STDOUT
from pathlib import Path

formatter = 'clang-format --style=file:utils/.clang-format'

def format_code(code : str) -> str:
	p = Popen(formatter.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
	return p.communicate(input=code.encode())[0].decode()

def modify_text(text : str) -> str:
	res = ''
	p = 0
	while True:
		start = text.find('```cpp', p)
		if start == -1:
			break
		end = text.find('```', start + 6)
		code = format_code(text[start+7:end-1])
		res += text[p:start]  + '```cpp\n' + code + '\n```'
		p = end + 3
	res += text[p:]
	return res

def modify_file(file : Path) -> None:
	file.write_text(modify_text(file.read_text()))


for file in Path('.').rglob('*.md'):
	modify_file(file)