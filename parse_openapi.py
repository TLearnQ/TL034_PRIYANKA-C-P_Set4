import yaml
import json
import requests
from collections import Counter

from logger import get_logger
from api_client import APIResponseError

logger = get_logger("Parser")

#from forg am gtting it
OPENAPI_FILES = {
    "NRF": "https://forge.3gpp.org/rep/all/5G_APIs/-/raw/REL-18/TS29510_Nnrf_NFManagement.yaml",
    "UDM": "https://forge.3gpp.org/rep/all/5G_APIs/-/raw/REL-18/TS29503_Nudm_SDM.yaml",
    "AMF": "https://forge.3gpp.org/rep/all/5G_APIs/-/raw/REL-18/TS29518_Namf_Communication.yaml",
    "SMF": "https://forge.3gpp.org/rep/all/5G_APIs/-/raw/REL-18/TS29502_Nsmf_PDUSession.yaml",
    "PCF": "https://forge.3gpp.org/rep/all/5G_APIs/-/raw/REL-18/TS29512_Npcf_SMPolicyControl.yaml"
}

def load_yaml(url, name):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        logger.info(f"{name} YAML loaded")
        return yaml.safe_load(resp.text)
    except Exception:
        logger.error(
            f"Failed to load YAML for {name}",
            extra={"error_code": "YAML_LOAD_ERROR"}
        )
        raise

def extract_endpoints(api, spec):
    endpoints = []
    paths = spec.get("paths")

    if not paths:
        raise APIResponseError("No paths found", "NO_PATHS")

    for path, ops in paths.items():
        for method, data in ops.items():
            if not isinstance(data, dict):
                continue

            responses = data.get("responses")
            if not responses:
                raise APIResponseError(
                    f"Missing responses for {method} {path}",
                    "MISSING_RESPONSE"
                )

            endpoints.append({
                "api": api,
                "path": path,
                "method": method.upper(),
                "summary": data.get("summary"),
                "response_codes": list(responses.keys()),
                "security": data.get("security")
            })

    return endpoints

def main():
    all_endpoints = []

    for api, url in OPENAPI_FILES.items():
        spec = load_yaml(url, api)
        try:
            all_endpoints += extract_endpoints(api, spec)
        except APIResponseError as e:
            logger.error(str(e), extra={"error_code": e.error_code})

    json.dump(all_endpoints, open("metadata.json", "w"), indent=2)
    logger.info("metadata.json generated")

    methods = Counter(ep["method"] for ep in all_endpoints)

    #summary= The summary should be generated


if __name__ == "__main__":
    main()
