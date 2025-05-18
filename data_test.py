shop_filter = {
    "articleType": [1, 2, 3],
    "baseColour": [4, 5, 6],
    "Made In": [7, 8, 9]
}
for variable in shop_filter:
    if variable:  # if list not empty
        print(variable, shop_filter[variable])
