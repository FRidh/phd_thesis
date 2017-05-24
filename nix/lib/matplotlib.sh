# Note that we do not use a phase because the hook is
# used with runCommand

# preConfigurePhases+=" matplotlibPhase"

# matplotlibPhase() {
runHook preMatplotlib
export FONTCONFIG_FILE=@fontsConf@
export HOME=$(readlink -f ".");
echo $FONTCONFIG_FILE
echo $HOME
runHook postMatplotlib
# }
