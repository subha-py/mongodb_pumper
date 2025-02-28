def human_read_to_byte(size):
    # if no space in between retry
    size_name = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")
    i = 0
    while i < len(size):
        if size[i].isnumeric():
            i += 1
        else:
            break
    size = size[:i], size[i:]              # divide '1 GB' into ['1', 'GB']
    num, unit = int(size[0]), size[1]
    idx = size_name.index(unit)
    # index in list of sizes determines power to raise it to
    factor = 1024 ** idx
    # ** is the "exponent" operator - you can use it instead of math.pow()
    return num * factor
def get_number_of_rows_from_size(size):
    # 8184701 documents = 2.00GB
    return int(8184701/human_read_to_byte('2G') * human_read_to_byte(size))

if __name__ == '__main__':
    rows = get_number_of_rows_from_size('25G')
    print(rows)