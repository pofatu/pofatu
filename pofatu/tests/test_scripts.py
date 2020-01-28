from pofatu.scripts.initializedb import main, prime_cache


def test_dbinit(db):
    main(None)
    prime_cache(None)
