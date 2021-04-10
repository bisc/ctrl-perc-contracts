@echo off
Setlocal enabledelayedexpansion

Set "Pattern=oleg"
Set "Replace=int"

For %%# in ("*") Do (
    Set "File=%%~nx#"
    Ren "%%#" "!File:%Pattern%=%Replace%!"
)

Pause&Exit