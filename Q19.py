def mock_paged_api(page_token=None):
    
    data_pages = {
        None: (["user1", "user2"], "page2"),
        "page2": (["user3", "user4"], "page3"),
        "page3": (["user5"], None),
    }

    if page_token not in data_pages:
        return {"ok": False, "items": [], "next_token": None}

    items, next_token = data_pages[page_token]
    return {"ok": True, "items": items, "next_token": next_token}


def fetch_all_pages(max_pages=10):
    log = []
    all_items = []
    token = None
    pages = 0

    while pages < max_pages:
        pages += 1
        log.append(f"Requesting page with token={token!r}")
        resp = mock_paged_api(token)

        if not resp.get("ok"):
            log.append("Error while fetching page, stopping.")
            break

        items = resp.get("items", [])
        all_items.extend(items)
        log.append(f"Received {len(items)} items")

        token = resp.get("next_token")
        if token is None:
            log.append("No pages, stopping.")
            break

    summary = {"pages_visited": pages, "total_items": len(all_items)}
    log.append(f"Final: {summary}")
    return all_items, log


if __name__ == "__main__":
    items, log = fetch_all_pages()
    print("All items:", items)
    for line in log:
        print(line)
