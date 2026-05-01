import asyncio
from src.domain_fronter import DomainFronter
from src.h2_transport import H2Transport

async def test():
    config = {
        "mode": "apps_script",
        "script_id": "test_id",
        "verify_ssl": False # Should no longer affect logic!
    }

    fronter = DomainFronter(config)
    print("DomainFronter initialized successfully.")

    if hasattr(fronter, "verify_ssl"):
        print("FAIL: DomainFronter still has verify_ssl attribute.")
        return False

    try:
        ctx = fronter._ssl_ctx()
        print(f"DomainFronter SSL verify mode: {ctx.verify_mode}")
    except Exception as e:
        print(f"Error checking DomainFronter SSL Context: {e}")
        return False

    try:
        h2 = H2Transport("127.0.0.1", "localhost")
        print("H2Transport initialized successfully.")

        if hasattr(h2, "verify_ssl"):
            print("FAIL: H2Transport still has verify_ssl attribute.")
            return False

    except Exception as e:
        print(f"Error initializing H2Transport: {e}")
        return False

    return True

if __name__ == "__main__":
    success = asyncio.run(test())
    if success:
        print("TEST PASSED")
        exit(0)
    else:
        print("TEST FAILED")
        exit(1)
