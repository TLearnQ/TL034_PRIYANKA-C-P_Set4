def process_log_lines(lines):
    

    audit = []   
    errors = 0
    processed = 0

    for line in lines:
        processed += 1
        try:
            text = line.strip()
            if text.startswith("ERROR") or text.startswith("WARN"):
                audit.append(text)
                if text.startswith("ERROR"):
                    errors += 1
        except Exception as e:
            


            audit.append(f"PROCESSING_ERROR: {e}")

    summary = {
        "processed": processed,
        "audit_count": len(audit),
        "error_count": errors,
    }
    return audit, summary


if __name__ == "__main__":
    sample = ["INFO: connection successful", "ERROR: timeout", "INFO: Retry"]
    audit, summary = process_log_lines(sample)
    print("AUDIT LINES:")
    for line in audit:
        print(line)
    print("SUMMARY:", summary)
