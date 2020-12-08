def formatnumber(number,ndigits=2):
    # Format the number with 2 digits behind the comma
    number = round(number, ndigits)
    numberparts = str(number).split('.')

    # Format the number before the comma with a space as 1000 seperator
    l = len(numberparts[0]) - 1
    blocks = int(l / 3)
    offset = len(numberparts[0]) % 3

    if (offset == 0):
        output = numberparts[0][:3]
    else:
        output = numberparts[0][:offset]

    for r in range(blocks):
        output += ' '
        output += numberparts[0][offset:offset + 3]
        offset += 3

    # If numbers has decimals
    if len(numberparts) == 2:
        output = output + "," + numberparts[1]

    return output


print(formatnumber(1933.213))