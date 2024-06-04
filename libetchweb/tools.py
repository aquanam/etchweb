OUTPUT: str | None = None
PRINT: bool = True


def writemsg(*args,
             sep: str = " ",
             end: str = "\n",
             enforce_no_print: bool = True) -> None:
    """Write message."""
    if PRINT or (not PRINT and not enforce_no_print):
        print(*args,
              sep=sep,
              end=end,
              file=OUTPUT)
