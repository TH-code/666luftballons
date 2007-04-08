; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=666 Luftballons
AppVerName=666 Luftballons 0.3
AppPublisher=Gin 'n Python
DefaultDirName={pf}\666 Luftballons
DefaultGroupName=666 Luftballons
LicenseFile=gpl.txt
OutputDir=installer
OutputBaseFilename=setup
Compression=lzma
SolidCompression=true
WizardImageFile=data\graphics\installer.bmp

[Languages]
Name: english; MessagesFile: compiler:Default.isl

[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked
Name: quicklaunchicon; Description: {cm:CreateQuickLaunchIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked

[Files]
Source: dist\*; DestDir: {app}; Flags: ignoreversion recursesubdirs

[Icons]
Name: {group}\666 Luftballons; Filename: {app}\666luftballons.exe
Name: {group}\{cm:UninstallProgram,666 Luftballons}; Filename: {uninstallexe}
Name: {commondesktop}\666 Luftballons; Filename: {app}\666luftballons.exe; Tasks: desktopicon
Name: {userappdata}\Microsoft\Internet Explorer\Quick Launch\666 Luftballons; Filename: {app}\666luftballons.exe; Tasks: quicklaunchicon

[Run]
Filename: {app}\666luftballons.exe; Description: {cm:LaunchProgram,666 Luftballons}; Flags: nowait postinstall skipifsilent
