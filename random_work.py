def longestCommonPrefix(strs) -> str:
    prefix = ""

    while not any([word == "" for word in strs]):
        letter = strs[0][0]
        if any(word[0] != letter for word in strs[1:]):
            return prefix
        else:
            prefix = prefix + letter

        for i in range(len(strs)):
            strs[i] = strs[i][1:]

    return prefix

print(longestCommonPrefix(["flower", "flowers", "flow", "flight"]))
