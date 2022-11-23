#pragma once

#include <QMap>
#include <QDebug>

struct FSMNode
{    
    int id;

    std::function<void()> entryAction;
    std::function<void()> exitAction;

    QMap<int, std::function<void()>> eventActions;

    QMap<int, int> transitions;
};

class FSMBase
{
public:
    explicit FSMBase() {

    }

    int currentStateId() const
    {
        return _currentStateId;
    }

    void postEvent(int eventId)
    {
        _handleEvent(eventId);
    }

protected:
    QString _fsmName;
    QMap<int, FSMNode> _fsmNodeTab;
    int _currentStateId;

private:
    void _handleEvent(int eventId)
    {
        if(_fsmNodeTab[_currentStateId].eventActions.contains(eventId)) {
            doEventAction(eventId);
        }
        _handleTransition(eventId);
    }

    void _handleTransition(int eventId)
    {
        if(_fsmNodeTab[_currentStateId].transitions.contains(eventId)) {
            doExitAction();
            _goToState(_fsmNodeTab[_currentStateId].transitions[eventId]);
        }
    }

    void doEventAction(int eventId)
    {
        _fsmNodeTab[_currentStateId].eventActions[eventId]();
    }

    void doEntryAction()
    {
        _fsmNodeTab[_currentStateId].entryAction();
    }

    void doExitAction()
    {
        _fsmNodeTab[_currentStateId].exitAction();
    }

    void _goToState(int stateId)
    {
        qDebug() << _fsmName << "go to state:" << stateId;

        _currentStateId = stateId;
        doEntryAction();
    }
};

