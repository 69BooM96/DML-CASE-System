text = ''''''

data = {}
osbm = False
osb = ""
word = ""
sb_list = [" ", "   ", "\n", ".", ",", "(", ")", "[", "]", "{", "}"]

for i in text:
    if osb == i:
        word +=i
        osbm = True
    else:
        if osbm: 
            word += word[-1]
            if word not in data: data[word] = 1
            else: data[word] = data[word]+1
            word = ""

        if i in sb_list:
            if word not in data:
                rw = []
                if len(word) > 4:
                    old_a = 0
                    for n in range(1, 5):
                        lsb = word[n:len(word)-old_a]
                        lsbt = word[n:]
                        rsb = word[old_a:len(word)-n]
                        rsbt = word[:len(word)-n]

                        if data.get(lsb) is not None and len(lsb) > 3: rw.append(lsb)
                        elif data.get(lsbt) is not None and len(lsbt) > 3: rw.append(lsbt)
                        elif data.get(rsb) is not None and len(rsb) > 3: rw.append(rsb)
                        elif data.get(rsbt) is not None and len(rsbt) > 3: rw.append(rsbt)

                        old_a = n
                if len(rw) > 0: data[rw[0]] = data[rw[0]]+1
                else: data[word] = 1
            else: data[word] = data[word]+1
            word = ""
        else:
            word+=i
        osbm = False
    osb = i


data.pop("", None)
repeats = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

for frag, count in repeats.items():
    print(f"{frag!r} -> {count}")