def contentq(content,*,split=True):
    if " " not in content:
        return ""
    while content.startswith(" ")==False:
        content=content[1:]
    while content.startswith(" "):
        content=content[1:]
    while "  " in content:
        content=content.replace("  "," ")
    content=content.split(" ")
    l=[]
    for w in content:
        l+=w.split("\n")
    if split:
        return content
    else:
        return " ".join(content)