{ python
, runCommand
, fetchurl
, matplotlibHook
}:

# Several audio files and spectrograms from the listening test stimuli.
# We cannot put all of them in the thesis.


let
  name = "listening";
in rec {

  # Some audio files taken from the listening test tarball.
  audio = let
    kind = "audio";
    # Tarball with listening test data.
    data = fetchurl {
      url = https://zenodo.org/record/376263/files/test.tar.gz;
      sha256 = "1zg9yg794g3wk2kqv259134hlkd5rwqib8zvlvwz70589cc1pism";
    };
  in runCommand "${name}-${kind}" {
    preferLocalBuild = true;
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    # Unpack to build dir
    tar -xzf ${data} -C .
    # Select files we want to keep
    cp stimuli/*11_103_A320*.wav "$out/${kind}/generated/${name}/"
#     tar -xzf ${data} -C "$out/"
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
