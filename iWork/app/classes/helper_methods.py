class Helper():
    def remove_duplicates(items):
        seen = set()
        unique_items = []
        for item in items:
            # Create a tuple of the item values for hashing
            item_tuple = tuple(item.items())
            if item_tuple not in seen:
                seen.add(item_tuple)
                unique_items.append(item)
        return unique_items