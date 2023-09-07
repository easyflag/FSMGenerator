#pragma once

#include <QDebug>

struct FSMNode
{
    int stateId;

    std::function<void()> entryAction;
    std::function<void()> exitAction;

    QMap<int, std::function<void()>> eventActions;

    QMap<int, int> transitions;
};

class FSMBase : public QObject
{
    Q_OBJECT

public:
    explicit FSMBase(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

    int currentStateId() const
    {
        return _currentStateId;
    }

    void postEvent(int eventId)
    {
        _handleEvent(eventId);
    }

    void setOutputLog(bool newOutputLog)
    {
        _outputLog = newOutputLog;
    }

signals:
    void currentStateIdChanged();

protected:
    QString             _fsmName;
    QMap<int, FSMNode>  _fsmNodes;
    int                 _currentStateId;
    bool                _outputLog{true};

private:
    void _handleEvent(int eventId)
    {
        if (_fsmNodes[_currentStateId].eventActions.contains(eventId)) {
            _doEventAction(eventId);
        }
        _handleTransition(eventId);
    }

    void _handleTransition(int eventId)
    {
        if (_fsmNodes[_currentStateId].transitions.contains(eventId)) {
            _doExitAction();
            _goToState(_fsmNodes[_currentStateId].transitions[eventId]);
        }
    }

    void _doEventAction(int eventId)
    {
        _fsmNodes[_currentStateId].eventActions[eventId]();
    }

    void _doEntryAction()
    {
        if (_fsmNodes[_currentStateId].entryAction)
            _fsmNodes[_currentStateId].entryAction();
    }

    void _doExitAction()
    {
        if (_fsmNodes[_currentStateId].exitAction)
            _fsmNodes[_currentStateId].exitAction();
    }

    void _goToState(int stateId)
    {
        if (_outputLog)
            qDebug() << _fsmName << "state from" << _currentStateId << "to" << stateId;

        _currentStateId = stateId;
        emit currentStateIdChanged();
        _doEntryAction();
    }
};
