{ python
, runCommand
, fetchurl
, matplotlibHook
, listening-test-tests
}:

# Several audio files and spectrograms from the listening test stimuli.
# We cannot put all of them in the thesis.


let
  name = "listening";
in rec {

  # Some audio files taken from the listening test tarball.
  audio = let
    kind = "audio";
  in runCommand "${name}-${kind}" {
    preferLocalBuild = true;
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    # Unpack to build dir
    tar -xzf ${listening-test-tests} -C .
    # Select files we want to keep
    cp stimuli/*11_103_A320*.wav "$out/${kind}/generated/${name}/"
  '';

  figures = let
    kind = "figures";
  in runCommand "${name}-${kind}" {
    buildInputs = [
      (python.withPackages (ps: with ps; [ acoustics matplotlib] ) )
      matplotlibHook
    ];
    preferLocalBuild = true;
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    python3 ${./figures.py} ${audio}/audio/generated/${name} "$out/${kind}/generated/${name}"
  '';
}
