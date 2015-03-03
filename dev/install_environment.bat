mkdir "C:\RestafariEnvironment"
cd "C:\RestafariEnvironment"
@powershell -NoProfile -ExecutionPolicy unrestricted -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin
choco install wget -y
wget -c -O atom_setup.exe --no-check-certificate "https://atom.io/download/windows"
atom_setup.exe /quiet
"%APPDATA%\..\Local\atom\bin\apm.cmd" install script
choco install git -y
choco install python -y
choco install easy.install -y
easy_install.exe PyYAML colorclass anyjson pycurl
git clone https://github.com/manoelhc/restafari.git
@echo "%APPDATA%\..\Local\atom\bin\atom.cmd" restafari > C:\RestafariEnvironment\OpenInAtom.bat
C:\RestafariEnviroment\OpenInAtom.bat
