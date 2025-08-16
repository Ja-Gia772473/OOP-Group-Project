"""
Product operations module for Smart Inventory Management System.
This module defines functions to find, search, remove and edit products
without modifying the original Main file.

Assumptions:
- Each product object has attributes `product_id`, `name`, `category`, `price`,
  `quantity`, and `reorder_level` or corresponding getter/setter methods.
- Category indices are integers 0-9 as per existing Main file mapping.
"""

def product_index(products, product_id):
    """Return the index of a product with the given ID in the list, or -1 if not found."""
    target = str(product_id).strip().lower()
    for i, p in enumerate(products):
        pid = ''
        # Attempt to get product id via attribute or getter
        if hasattr(p, 'product_id'):
            pid = str(p.product_id)
        elif hasattr(p, 'get_product_id'):
            try:
                pid = str(p.get_product_id())
            except Exception:
                pass
        if pid.strip().lower() == target:
            return i
    return -1

def search_product(products, term):
    """Return a list of products whose name or category name contains the search term (case-insensitive)."""
    if not term:
        return []
    q = term.strip().lower()
    results = []
    # Mapping of category indices to names (0-9)
    categories = {
        0: "Electronics",
        1: "Clothing",
        2: "Home",
        3: "Grocery",
        4: "Books",
        5: "Toys",
        6: "Sports",
        7: "Beauty",
        8: "Automotive",
        9: "Others"
    }
    for p in products:
        # Determine name
        name = ''
        if hasattr(p, 'name'):
            name = str(p.name)
        elif hasattr(p, 'get_name'):
            try:
                name = str(p.get_name())
            except Exception:
                name = ''
        # Determine category name
        category_name = None
        if hasattr(p, 'get_category_name'):
            try:
                category_name = p.get_category_name()
            except Exception:
                category_name = None
        if category_name is None and hasattr(p, 'category'):
            cat_index = p.category
            category_name = categories.get(cat_index, str(cat_index))
        # Compare
        if q in name.lower() or (category_name and q in str(category_name).lower()):
            results.append(p)
    return results

def remove_product(products):
    """Prompt for a product ID, remove the matching product from the list, and display the removed product or an error message."""
    pid = input("Enter product ID to remove: ").strip()
    idx = product_index(products, pid)
    if idx == -1:
        print("Product not found.")
        return
    removed = products.pop(idx)
    print(f"Removed: {removed}")

def edit_product(products):
    """Prompt for a product ID, then allow editing name, category, price and reorder level. Leave blank to keep current values."""
    pid = input("Enter product ID to edit: ").strip()
    idx = product_index(products, pid)
    if idx == -1:
        print("Product not found.")
        return
    p = products[idx]
    print("\nLeave blank to keep current value.")
    # Update name
    current_name = getattr(p, 'name', '')
    new_name = input(f"Name [{current_name}]: ").strip()
    if new_name:
        if hasattr(p, 'set_name'):
            try:
                p.set_name(new_name)
            except Exception:
                p.name = new_name
        else:
            p.name = new_name
    # Update category (0-9)
    current_category = getattr(p, 'category', None)
    new_cat = input(f"Category index 0-9 [{current_category}]: ").strip()
    if new_cat:
        try:
            c = int(new_cat)
            if 0 <= c <= 9:
                if hasattr(p, 'set_category'):
                    try:
                        p.set_category(c)
                    except Exception:
                        p.category = c
                else:
                    p.category = c
            else:
                print("Invalid category; unchanged.")
        except ValueError:
            print("Invalid category; unchanged.")
    # Update price
    current_price = getattr(p, 'price', 0)
    new_price = input(f"Price [{current_price}]: ").strip()
    if new_price:
        try:
            val = float(new_price)
            if val >= 0:
                if hasattr(p, 'set_price'):
                    try:
                        p.set_price(val)
                    except Exception:
                        p.price = val
                else:
                    p.price = val
            else:
                print("Invalid price; unchanged.")
        except ValueError:
            print("Invalid price; unchanged.")
    # Update reorder level
    current_rl = getattr(p, 'reorder_level', 0)
    new_rl = input(f"Reorder level [{current_rl}]: ").strip()
    if new_rl:
        try:
            rl = int(new_rl)
            if rl >= 0:
                if hasattr(p, 'set_reorder_level'):
                    try:
                        p.set_reorder_level(rl)
                    except Exception:
                        p.reorder_level = rl
                else:
                    p.reorder_level = rl
            else:
                print("Invalid reorder level; unchanged.")
        except ValueError:
            print("Invalid reorder level; unchanged.")
    print("Product updated.")
