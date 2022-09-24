#pragma once

#include <QObject>

struct FSMNode
{
    int stateId;
    
    std::function<void()> actionOnEnter;
    std::function<void()> actionOnExit;
};

class FSMengine : public QObject
{
    Q_OBJECT
public:
    explicit FSMengine(QObject *context = nullptr);

    void createFSMFromFile(QString filename);
    
    void registerEnterAction(int stateId, std::function<void()> action);
    void registerExitAction(int stateId, std::function<void()> action);

    void postEvent(int eventId);
    

signals:
    
private:
    QObject *_context = nullptr;

    QList<int> states;
    QList<int> events;
    QList<QList<FSMNode>> _FSMDefTab;
};

