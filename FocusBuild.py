import os
import sys
import subprocess
import re
import glob

consoleOutput = []


def main(filePath):
    global consoleOutput
    pathParts = filePath.split('\\')
    pathDict = {
        'magic' : 'C:\\Program Files (x86)\\MEDITECH',
        # 'data'  : '\\'.join(pathParts[0:pathParts.index('MEDITECH') + 1]),
        'unv'   : 'MTUNV616.Universe\\D6.16F.Ring',
        # 'rem'   : '\\'.join(pathParts[pathParts.index('!AllUsers') + 1:-1]),
        'name'  : pathParts[-1],
        'file'  : filePath,
        'exe'   : 'System\\magic.exe',
        'tools' : 'System\\PgmObject\\FocZ.TextPadTools.P.mps',
        'format': 'System\\PgmObject\\FocZ.Format.P.mps',
        'lint'  : 'M-AT Tools\\M-AT_Code_Checker\\at_code_checker.exe',
        'xlate' : 'System\\Translators\\Translator.mas',
        'user'  : 'PTIROFF'
    }
    t = format(pathDict) and lint(pathDict) and translate(pathDict)
    print(pathDict['name'])
    printOutput()
    consoleOutput = []
    return t


def format(d):
    global consoleOutput
    try:
        subprocess.check_output('"{magic}\\{unv}\\{exe}" "{magic}\\{unv}\\{tools}" FORMAT "{file}"'.format(**d), False)
    except subprocess.CalledProcessError as e:
        consoleOutput += getLines(e.output)
        return False

    consoleOutput.append('    >Format: Success')
    return True


def lint(d):
    global consoleOutput
    try:
        subprocess.check_output('"{magic}\\{lint}" "{file}"'.format(**d), False)
    except subprocess.CalledProcessError as e:
        consoleOutput += getLines(e.output)
        return False

    consoleOutput.append('    >Lint: Success')
    return True


def translate(d):
    global consoleOutput
    try:
        subprocess.check_output('"{magic}\\{unv}\\{exe}" "{magic}\\{unv}\\{xlate}" "{file}" /error:stdout /codebase:InPlace'.format(**d), False)
    except subprocess.CalledProcessError as e:
        consoleOutput.append('>Translate:')
        consoleOutput += ['\t'.join(re.split(' - ', x, 1)) for x in getLines(e.output) if x != '']
        return False

    moveFiles(d)
    consoleOutput.append('    >Translate: Success')
    return True


def moveFiles(d):
    global consoleOutput
    fileBase = os.path.splitext(d.get('file'))[0]
    for translationFile in glob.glob(fileBase + '.m*s'):
        target = fileBase.replace('PgmSource', 'Translations') + os.path.splitext(translationFile)[1]
        #Remove the application folder
        target, filename = os.path.split(target)
        target = os.path.join(os.path.split(target)[0], filename)
        if(os.path.isfile(target)):
            os.remove(target)
        try:
            os.rename(translationFile, target)
        except OSError as e:
            consoleOutput += getLines(e.strerror)

    return True


def getLines(string):
    try:
        string = string.decode()
    except AttributeError:
        pass
    return re.split('\r\n|\r|\n', string)


def printOutput(lines=consoleOutput):
    global consoleOutput
    for line in lines:
        print(line)

    return True


if(__name__ == "__main__"):
    main(sys.argv[1])
