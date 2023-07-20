#include <QApplication>

#include "ClampFSM.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QFile *file = new QFile("1.txt");
    qDebug() << file->open(QIODevice::WriteOnly | QIODevice::Text);
    ClampFSM f(file);
    f.postEvent(ClampFSMDef::To_Loose);
    f.postEvent(ClampFSMDef::To_Tight);
    file->close();
    delete file;

    app.exec();
}
