import httpx

class InternalHttpClient:
    def __init__(self, base_url: str = "http://localhost:8002") -> None:
        self._client = httpx.Client(
            base_url=base_url
        )

    def verify_domain(self, domain_id: str, account_id: str = "e6cc89f4-432d-466f-8032-3b2a3484a4b2") -> None:
        credential_json = {
            "clientId": "dc1b9ac1-dd00-44a9-88c0-47e7d193c709",
            "clientSecret": "019634d1-bc75-7000-a2b5-5f002e0361de"
        }
        credential_response = self._client.request("POST", "/internal/client-credentials/token", json=credential_json, headers={
            "Content-Type": "application/json"
        })
        if credential_response.status_code != 200:
            raise Exception(f"Received status code {credential_response.status_code} from credential endpoint")

        cred_resp_json = credential_response.json()
        token = cred_resp_json["accessToken"]
        domain_resp = self._client.request(
            "POST",
            "/internal/test-helpers/domains/verify",
            json={"id": domain_id, "accountId": account_id},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        if domain_resp.status_code != 204:
            raise Exception(f"Received status code {domain_resp.status_code} from domain verification endpoint")