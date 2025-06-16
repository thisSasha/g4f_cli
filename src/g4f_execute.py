import io, threading, logging, re, time

g4f = None
logger = None
print_toCopy = None
DEBUG = None
general_allModels = {}

def setup_g4f(g4f_, logger_, print_toCopy_, DEBUG_):
    global g4f, logger, print_toCopy, general_allModels, DEBUG
    g4f = g4f_
    logger = logger_
    print_toCopy = print_toCopy_
    DEBUG = DEBUG_


def g4f_find(typeToFind, keysRule, keys):
    founded = []

    if typeToFind == "provider":
        for provider in g4f.Provider.__all__:
            if _check_rules(provider, keysRule, keys):
                founded.append(provider)
    elif typeToFind == "model":
        models = g4f.models._all_models
        for model in models:
            if _check_rules(model, keysRule, keys):
                founded.append(model)

    logger.info("Founded:")
    print_toCopy(founded)


def _check_rules(model, keysRule, keys):
    return (
        all(key.lower() in model.lower() for key in keys)
        if keysRule == "and"
        else any(key.lower() in model.lower() for key in keys)
    )


def g4f_call(model, provider, msg):
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter("%(name)s - %(message)s"))
    handler.setLevel(logging.DEBUG)

    target_names = [
        "g4f",
        "undetected_chromedriver",
        "urllib3",
        "websockets",
        "nodriver",
    ]

    prev = {}
    for name in target_names:
        lg = logging.getLogger(name)
        prev[name] = lg.disabled
        lg.disabled = False
        lg.setLevel(logging.DEBUG)
        lg.addHandler(handler)

    result = {}
    error = {}

    def worker():
        try:        
            result["data"] = g4f.ChatCompletion.create(
                model=g4f.models.__dict__.get(model),
                provider=g4f.Provider.__dict__.get(provider),
                messages=[{"role": "user", "content": msg}],
            )
        except Exception as ex:
            error["err"] = ex
            error["fileName"] = ex.__traceback__.tb_frame.f_code.co_filename
            error["line"] = ex.__traceback__.tb_lineno

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    warn_logged = 0
    delay_warned = False

    try:
        counter = 0
        while thread.is_alive():
            time.sleep(1)
            counter += 1
            logs = log_stream.getvalue()
            if DEBUG:
                open(".log", "w").write(logs)

            undefined = len(
                re.findall(r"nodriver\.core\.connection.*'type': 'undefined'", logs)
            )
            config_fail = len(
                re.findall(r"nodriver\.core\.config.*not a valid candidate", logs)
            )
            config_ok = bool(
                re.search(r"nodriver\.core\.config.*is a valid candidate", logs)
            )
            browser_ready = bool(
                re.search(r"nodriver\.core\.browser.*Session object initialized", logs)
            )

            if (
                config_fail > 1
                and not config_ok
                and counter > 1
                and warn_logged < config_fail
            ):
                warn_logged = config_fail
                logger.warning(f"Browser path attempts: {config_fail}")

            if config_ok and counter > 10 and not browser_ready and counter % 5 == 0:
                logger.warning("Browser startup delayed")

            if undefined % 5 == 0 and undefined > 0:
                logger.warning("Browser unresponsive, retrying...")

            if undefined > 10:
                logger.error("Browser not responding or hung")
                logger.info("Try enabling VPN")
                return
    finally:
        for name in target_names:
            lg = logging.getLogger(name)
            lg.disabled = prev[name]
            lg.removeHandler(handler)
        handler.close()

    if "err" in error:
        raise TypeError(f"{error['err']} at {error['fileName']}:{error['line']}")

    print(result.get("data"))


def g4f_get(entity_type, entity_name):
    if entity_type == "providers":
        got = general_allModels.get(entity_name, [])
    elif entity_type == "models":
        got = [
            model
            for model, providers in general_allModels.items()
            if entity_name in providers
        ]
    else:
        got = []

    logger.info(f"Found {entity_type} for {entity_name}:")
    print_toCopy(got.copy())


def g4f_getAll(entity_type):
    entities = []
    if entity_type == "providers":
        entities = g4f.Provider.__all__
    elif entity_type == "models":
        entities = g4f.models._all_models
    logger.info(f"All g4f {entity_type}:")
    print_toCopy(list(entities))


def g4f_getProviders(model_name):
    providers = []
    model = getattr(g4f.models, model_name, None)
    if not model:
        logger.error(f"Model '{model_name}' not found.")
        return providers

    best_provider = getattr(model, "best_provider", None)
    base_provider = getattr(model, "base_provider", None)

    if best_provider and hasattr(best_provider, "providers"):
        providers.extend(best_provider.providers)
    if base_provider:
        providers.append(base_provider)

    unique_labels = set()
    for provider in providers:
        label = _extract_label(provider)
        if label not in unique_labels:
            unique_labels.add(label)

    return unique_labels


def _extract_label(provider):
    if type(provider) == str:
        return provider
    else:
        return (
            provider.__dict__.get("label")
            if provider.__dict__.get("label")
            else str(provider).split(".")[-1].replace("_", " ").replace("'>", "")
        )


def g4f_setAllModels():
    global general_allModels

    models = g4f.models.__dict__
    realModels = []
    for model in models.keys():
        if isinstance(models.get(model), g4f.Model):
            realModels.append(model)
    for model in realModels:
        general_allModels[model] = g4f_getProviders(model)
    return general_allModels
