

# unsuccessful experiment
def transactional(func, session):
    def func_wrapper(*args, **kwargs):
        try:
            data, status = func(*args, **kwargs)
        except Exception as e:
            session.rollback()
            raise e

        if 200 <= status < 300:
            session.commit()
        else:
            session.rollback()

    return func_wrapper
