# -------------------------------------------

class HTML:
    def __init__(self, output=None):
        self.output = output
        self.childrens = []

    def __add__(self, other):
        self.childrens.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        print("<html>")
        for child in self.childrens:
            print(child)
        print("</html>")

# -------------------------------------------------------------

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.childrens = []

    def __enter__(self):
        return self

    def __add__(self, child):
        self.childrens.append(child)
        return self

    def __str__(self):
        starting = "<{tag}>".format(tag=self.tag)
        internal = ""
        for child in self.childrens:
            internal += str(child)
        ending = "</{tag}>".format(tag=self.tag)

        return starting + internal + ending

    def __exit__(self, type, value, traceback):
        return self

# -----------------------------------------------------------------------

class Tag:
    def __init__(self, tag, klass=None, toplevel=False, is_single=False, **atrs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.toplevel = toplevel
        self.is_single = is_single
        self.children = []
        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        for attr, value in atrs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback,**atrs):
        if self.toplevel:
            print("<%s>\n" % self.tag)
            for child in self.children:
                print(child)
            print("</%s>\n" % self.tag)

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>\n".format(tag=self.tag, attrs=attrs)
            else:
                if len(attrs)==0:
                    return "<{tag}>{text}</{tag}>\n".format(tag=self.tag, text=self.text)
                else:
                    return "<{tag} {attrs}>{text}</{tag}>\n".format(tag=self.tag, attrs=attrs, text=self.text)